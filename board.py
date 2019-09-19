from figures import King, Queen, Rook, Bishop, Knight, Pawn
from params import WHITE, BLACK


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
        pass

    # Метод возвращает фигуру, стоящую на клетке r, c
    def get_figure(self, r, c):
        for figure in (self.pl_figures + self.cmp_figures):
            if figure.row == r and figure.col == c and not figure.is_drop:
                return figure
        return None
