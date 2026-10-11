import random
import time

from game_pack.figures import *
from game_pack.params import *

# Оценка мата: заведомо больше любой материальной оценки.
MATE_SCORE = 100000

# "Бесконечность" для границ alpha-beta.
INF = 1 << 30

# Проверка времени выполняется не на каждом узле, а раз в несколько тысяч
# узлов, чтобы не тратить время на вызовы time.time().
NODES_PER_TIME_CHECK = 1024

# Ограничение глубины поиска взятий (quiescence), чтобы размены не уходили
# в бесконечность.
QUIESCENCE_MAX_DEPTH = 4


class SearchTimeout(Exception):
    """Поиск прерван по истечении отведенного времени."""
    pass


class Ai:

    def __init__(self, side, board, time_budget=None, max_depth=None):
        self.side = side
        self.board = board
        self.time_budget = time_budget if time_budget is not None else AI_TIME_BUDGET
        self.max_depth = max_depth if max_depth is not None else AI_MAX_DEPTH

        self._deadline = None
        self._nodes = 0
        # Лучший ход предыдущей итерации углубления (для порядка ходов)
        self._pv_key = None

    # Метод возвращает следующий ход компьютера
    def get_next_move(self):
        # Получаем список доступных ходов
        avl_moves = self.board.get_all_avl_moves(self.side)

        moves_count = self.board.get_moves_count()
        random.seed()
        random_move = avl_moves[random.randint(0, len(avl_moves) - 1)]

        # Первый ход выбирается компьютером случайным образом
        if moves_count == 0 or moves_count == 1:
            return random_move

        # Итеративное углубление с ограничением по времени: ищем на глубину
        # 1, 2, 3, ... пока не выйдем за отведенный бюджет. Возвращаем лучший
        # ход последней полностью завершенной итерации.
        self._nodes = 0
        self._pv_key = None
        self._deadline = time.time() + self.time_budget

        best_move = random_move
        best_score = 0
        for depth in range(1, self.max_depth + 1):
            try:
                move, score = self._search_root(depth)
            except SearchTimeout:
                break
            if move is not None:
                best_move = move
                best_score = score
            # Если найден мат, дальше углубляться нет смысла
            if abs(best_score) >= MATE_SCORE - self.max_depth:
                break

        self._deadline = None
        return best_move

    # Публичный метод поиска на фиксированную глубину (используется в замерах)
    def search(self, depth):
        self._nodes = 0
        self._pv_key = None
        self._deadline = time.time() + self.time_budget
        return self._search_root(depth)

    # Проверка выхода за бюджет времени
    def _check_time(self):
        self._nodes += 1
        if self._nodes % NODES_PER_TIME_CHECK == 0 and time.time() >= self._deadline:
            raise SearchTimeout()

    # Поиск в корне дерева: возвращает (лучший ход, его оценку)
    def _search_root(self, depth):
        side = self.side
        moves = self.board.get_all_avl_moves(side)
        if not moves:
            return None, 0

        self._order_moves(moves, self._pv_key)

        alpha = -INF
        best_move = None
        best_score = -INF
        for move in moves:
            self._prepare(move, side)
            self.board.apply_move(move)
            try:
                score = -self._negamax(depth - 1, -INF, -alpha, OPPOSITE_SIDE[side], 1)
            finally:
                self.board.cancel_move()
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha:
                alpha = score

        if best_move is not None:
            self._pv_key = (best_move.old_row, best_move.old_col, best_move.new_row, best_move.new_col)
        return best_move, best_score

    # Негамакс с отсечением alpha-beta
    def _negamax(self, depth, alpha, beta, side, ply):
        self._check_time()

        if depth <= 0:
            return self._quiescence(alpha, beta, side, ply, 0)

        moves = self.board.get_all_avl_moves(side)
        if not moves:
            # Нет ходов: мат или пат
            if self.board.is_strike_figure(self.board.kings_dict[side]):
                return -MATE_SCORE + ply
            return 0

        best = -INF
        for move in moves:
            self._prepare(move, side)
            self.board.apply_move(move)
            try:
                score = -self._negamax(depth - 1, -beta, -alpha, OPPOSITE_SIDE[side], ply + 1)
            finally:
                self.board.cancel_move()
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        return best

    # Поиск затишья: на листьях перебираем только взятия и превращения,
    # чтобы избежать "горизонтального эффекта" на незавершенных разменах.
    def _quiescence(self, alpha, beta, side, ply, qdepth):
        self._check_time()

        if qdepth >= QUIESCENCE_MAX_DEPTH:
            return self.board.position_evaluation(side)

        in_check = self.board.is_strike_figure(self.board.kings_dict[side])
        if in_check:
            # Под шахом оценивать "как есть" нельзя, перебираем все ходы
            moves = self.board.get_all_avl_moves(side)
            if not moves:
                return -MATE_SCORE + ply
            best = -INF
        else:
            stand = self.board.position_evaluation(side)
            if stand >= beta:
                return stand
            if stand > alpha:
                alpha = stand
            best = stand
            moves = self._capture_moves(side)

        for move in moves:
            self._prepare(move, side)
            self.board.apply_move(move)
            try:
                score = -self._quiescence(-beta, -alpha, OPPOSITE_SIDE[side], ply + 1, qdepth + 1)
            finally:
                self.board.cancel_move()
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        return best

    # Возвращает список взятий и превращений для поиска затишья
    def _capture_moves(self, side):
        result = []
        for move in self.board.get_all_avl_moves(side):
            if move.m_type in (TAKE_MOVE, PASSED_TAKE, CONVERSION):
                result.append(move)
        return result

    # Для ходов-превращений создает фигуру, которой заменяется пешка
    @staticmethod
    def _prepare(move, side):
        if move.m_type == CONVERSION and move.new_figure is None:
            move.new_figure = Queen(move.new_row, move.new_col, side, move.figure.board)
        return move

    # Ставит ход предыдущей итерации в начало списка (улучшает отсечение)
    @staticmethod
    def _order_moves(moves, pv_key):
        if pv_key is None:
            return
        for index, move in enumerate(moves):
            if (move.old_row, move.old_col, move.new_row, move.new_col) == pv_key:
                moves.insert(0, moves.pop(index))
                return
