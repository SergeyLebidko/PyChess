from figures import King, Queen, Rook, Bishop, Knight, Pawn
from params import WHITE, BLACK, NORMAL_MOVE, TAKE_MOVE


class Move:

    def __init__(self, move_type):
        self.move_type = move_type


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

    # Метод возвращает список доступных для данной фигуры ходов
    def get_avl_moves_for_figure(self, figure):
        # Список ходов, который будем формировать
        moves = []

        figure_type = type(figure)

        # У пешек есть ряд отличительных особенностей, которые необходимо учитывать при получении доступных ходов:
        # - только пешки бьют и ходят на разные поля
        # - только у пешек есть взятие на проходе
        # - только пешка может превратиться в другую фигуру при достижении края поля
        # Поэтому код создания ходов для пешек отличается от кода создания ходов для других фигур
        if figure_type == Pawn:
            # Создаем обычные ходы пешки
            actions = figure.get_actions('moves')
            for new_row, new_col in actions:
                moves.append(self.create_normal_move(figure, new_row, new_col))
            # Создаем взятия
            actions = figure.get_actions('takes')
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    continue
                if drop_figure.side == figure.side:
                    continue
                moves.append(self.create_take_move(figure, new_row, new_col))
            # Здесь необходимо вставить код создания ходов:
            # - взятия на проходе
            # - превращения пешки в другую фигуру при достижении края доски

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

    # Метод применяет переданный ход и вносит его в список совершенных ходов
    def apply_move(self, move):
        pass

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
