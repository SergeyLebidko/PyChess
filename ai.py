import random
from figures import *
import sys


class Ai:

    def __init__(self, side, board):
        self.side = side
        self.board = board

        self.count = 0

    # Метод возвращает следующий ход компьютера
    def get_next_move(self):
        # Получаем список доступных ходов
        avl_moves = self.board.get_all_avl_moves(self.side)

        # Первый ход выбирается компьютером случайным образом
        moves_count = self.board.get_moves_count()
        if moves_count == 0 or moves_count == 1:
            random.seed()
            move = avl_moves[random.randint(0, len(avl_moves) - 1)]
            return move

        # Иначе нам нужно выбрать ход с максимальной оценкой
        self.count = 0

        max_rating = -sys.maxsize
        for move in avl_moves:
            self.board.apply_move(move)
            self.count += 1
            rating = self.get_rating(2, 'max', self.side, max_rating)
            self.board.cancel_move()
            if rating > max_rating:
                max_rating = rating
                move_with_max_rating = move

        # Возвращаем найденный ход
        print('Просмотрено ходов: ', self.count)
        return move_with_max_rating

    # Метод возвращает оценку хода
    # d - глубина рекурсии
    # option - что мы ищем на верхнем уровне (максимум или минимум)
    # side - сторона, для которой мы ищем максимум или минимум на верхнем уровне
    def get_rating(self, d, option, side, limit):
        if d == 0:
            return self.board.position_evaluation()

        if option == 'max':
            rating = sys.maxsize
        if option == 'min':
            rating = -sys.maxsize

        avl_moves = self.board.get_all_avl_moves(OPPOSITE_SIDE[side])
        for avl_move in avl_moves:
            self.board.apply_move(avl_move)
            self.count += 1
            if option == 'max':
                tmp_rating = self.get_rating(d - 1, 'min', OPPOSITE_SIDE[side], rating)
                if tmp_rating < limit:
                    self.board.cancel_move()
                    break
                rating = min(rating, tmp_rating)
            if option == 'min':
                tmp_rating = self.get_rating(d - 1, 'max', OPPOSITE_SIDE[side], rating)
                if tmp_rating > limit:
                    self.board.cancel_move()
                    break
                rating = max(rating, tmp_rating)
            self.board.cancel_move()

        return rating
