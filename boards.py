from figures import *


class Move:

    def __init__(self, move_type):
        self.m_type = move_type


class Board:

    def __init__(self, pl_side):
        self.pl_side = pl_side
        if pl_side == WHITE:
            self.cmp_side = BLACK
        if pl_side == BLACK:
            self.cmp_side = WHITE

        self.pl_figures = []
        self.cmp_figures = []

        # Создаем фигуры компьютера
        if self.cmp_side == WHITE:
            self.cmp_king = King(0, 3, self.cmp_side, self)
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 4, self.cmp_side, self))

        if self.cmp_side == BLACK:
            self.cmp_king = King(0, 4, self.cmp_side, self)
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 3, self.cmp_side, self))

        self.cmp_figures.append(Rook(0, 0, self.cmp_side, self))
        self.cmp_figures.append(Rook(0, 7, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 1, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 6, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 2, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 5, self.cmp_side, self))

        for i in range(0, 8):
            self.cmp_figures.append(Pawn(1, i, self.cmp_side, self))

        # Создаем фигуры игрока
        if self.cmp_side == WHITE:
            self.pl_king = King(7, 3, self.pl_side, self)
            self.cmp_figures.append(self.pl_king)
            self.cmp_figures.append(Queen(7, 4, self.pl_side, self))

        if self.cmp_side == BLACK:
            self.pl_king = King(7, 4, self.pl_side, self)
            self.cmp_figures.append(self.pl_king)
            self.cmp_figures.append(Queen(7, 3, self.pl_side, self))

        self.cmp_figures.append(Rook(7, 0, self.pl_side, self))
        self.cmp_figures.append(Rook(7, 7, self.pl_side, self))
        self.cmp_figures.append(Knight(7, 1, self.pl_side, self))
        self.cmp_figures.append(Knight(7, 6, self.pl_side, self))
        self.cmp_figures.append(Bishop(7, 2, self.pl_side, self))
        self.cmp_figures.append(Bishop(7, 5, self.pl_side, self))

        for i in range(0, 8):
            self.cmp_figures.append(Pawn(6, i, self.pl_side, self))

        # Создаем список сделанных во время игры ходов
        self.move_list = []

    # Метод возвращает все доступные ходы для выбранных фигур (белых или черных)
    def get_all_avl_moves(self, side):
        # Определяем набор фигур, для которого будем получать доступные ходы
        if side == self.pl_side:
            work_list = self.pl_figures
        if side == self.cmp_side:
            work_list = self.cmp_figures

        # Перебираем фигуры из набора
        result = []
        for figure in work_list:
            if figure.is_drop:
                continue
            avl_moves = self.get_avl_moves_for_figure(figure)
            result += avl_moves

        # Возвращаем результат
        return result

    # Метод возвращает список доступных для данной фигуры ходов
    def get_avl_moves_for_figure(self, figure):
        # Список ходов, который будем формировать
        moves = []

        figure_type = type(figure)

        # У пешек есть ряд отличительных особенностей, которые необходимо учитывать при получении доступных ходов:
        # - только пешки бьют и ходят на разные поля
        # - только у пешек есть взятие на проходе
        # - только пешка может превратиться в другую фигуру при достижении края поля (в том числе при взятии)
        # Поэтому код создания ходов для пешек отличается от кода создания ходов для других фигур
        if figure_type == Pawn:
            # Создаем обычные ходы и ход-конверсию при обычном ходе
            actions = figure.get_actions(PAWN_MOVES)
            for new_row, new_col in actions:
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_normal_move(figure, new_row, new_col))
            # Создаем взятия и ход-конверсию при взятии
            actions = figure.get_actions(PAWN_TAKES)
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    continue
                if drop_figure.side == figure.side:
                    continue
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_take_move(figure, new_row, new_col))

            # Здесь необходимо вставить код создания ходов:
            # - взятия на проходе

        # Получаем ходы других фигур
        if figure_type != Pawn:
            actions = figure.get_actions()
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    moves.append(self.create_normal_move(figure, new_row, new_col))
                    continue
                if drop_figure.side != figure.side:
                    moves.append(self.create_take_move(figure, new_row, new_col))

        # Здесь необходимо вставить код проверки возможности и создания рокировки, если figure_type == King

        # Здесь необходимо вставить код отсечения ходов, ведущих к шаху

        # Возвращаем результат
        return moves

    # Метод создает обычный ход
    @staticmethod
    def create_normal_move(figure, new_row, new_col):
        move = Move(NORMAL_MOVE)
        move.figure = figure
        move.old_row = figure.row
        move.old_col = figure.col
        move.new_row = new_row
        move.new_col = new_col
        return move

    # Метод создает ход-взятие
    def create_take_move(self, figure, new_row, new_col):
        move = Move(TAKE_MOVE)
        move.figure = figure
        move.old_row = figure.row
        move.old_col = figure.col
        move.new_row = new_row
        move.new_col = new_col
        move.drop_figure = self.get_figure(new_row, new_col)
        return move

    # Метод создает ход-конверсию
    def create_conversion_move(self, figure, new_row, new_col):
        move = Move(CONVERSION)
        move.figure = figure
        move.old_row = figure.row
        move.old_col = figure.col
        move.new_row = new_row
        move.new_col = new_col
        move.drop_figure = self.get_figure(new_row, new_col)
        move.new_figure = None
        return move

    # Метод применяет переданный ход и вносит его в список совершенных ходов
    def apply_move(self, move):
        # Вносим применяемый ход в список ходов
        self.move_list.append(move)

        # Выполняем действия хода в зависимости от его типа
        # Обычный ход
        if move.m_type == NORMAL_MOVE:
            move.figure.set_pos(move.new_row, move.new_col)
            return

        # Ход-взятие
        if move.m_type == TAKE_MOVE:
            move.figure.set_pos(move.new_row, move.new_col)
            move.drop_figure.is_drop = True
            return

        # Ход-конверсия
        if move.m_type == CONVERSION:
            move.figure.set_pos(move.new_row, move.new_col)
            move.figure.is_drop = True
            if move.drop_figure is not None:
                move.drop_figure.is_drop = True
            if move.new_figure.side == self.pl_side:
                self.pl_figures.append(move.new_figure)
                return
            if move.new_figure.side == self.cmp_side:
                self.cmp_figures.append(move.new_figure)
                return

    # Метод откатывает последний ход из списка совершенных ходов
    def cancel_move(self):
        if len(self.move_list) == 0:
            return
        pass

    # Метод возвращает фигуру, стоящую на клетке r, c
    def get_figure(self, r, c):
        for figure in (self.pl_figures + self.cmp_figures):
            if figure.row == r and figure.col == c and not figure.is_drop:
                return figure
        return None


class SelectorBoard:

    def __init__(self, side, main_board):
        self.queen = Queen(3, 3, side, main_board)
        self.rook = Rook(3, 4, side, main_board)
        self.bishop = Bishop(4, 3, side, main_board)
        self.knight = Knight(4, 4, side, main_board)

    def get_figure(self, r, c):
        if r == 3 and c == 3:
            return self.queen
        if r == 3 and c == 4:
            return self.rook
        if r == 4 and c == 3:
            return self.bishop
        if r == 4 and c == 4:
            return self.knight
