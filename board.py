from figures import King, Queen, Rook, Bishop, Knight, Pawn
from params import WHITE, BLACK


class Board:

    def __init__(self, player_side):
        self.player_side = player_side
        if player_side == WHITE:
            self.computer_side = BLACK
        if player_side == BLACK:
            self.computer_side = WHITE

        self.player_figures = []
        self.computer_figures = []

        # Создаем фигуры компьютера
        for i in range(0, 8):
            self.computer_figures.append(Pawn(1, i, self.computer_side))
        self.computer_figures.append(Rook(0, 0, self.computer_side))
        self.computer_figures.append(Rook(0, 7, self.computer_side))
        self.computer_figures.append(Knight(0, 1, self.computer_side))
        self.computer_figures.append(Knight(0, 6, self.computer_side))
        self.computer_figures.append(Bishop(0, 2, self.computer_side))
        self.computer_figures.append(Bishop(0, 5, self.computer_side))

        if self.computer_side == WHITE:
            self.computer_figures.append(King(0, 3, self.computer_side))
            self.computer_figures.append(Queen(0, 4, self.computer_side))

        if self.computer_side == BLACK:
            self.computer_figures.append(King(0, 4, self.computer_side))
            self.computer_figures.append(Queen(0, 3, self.computer_side))

        # Создаем фигуры игрока
        for i in range(0, 8):
            self.computer_figures.append(Pawn(6, i, self.player_side))
        self.computer_figures.append(Rook(7, 0, self.player_side))
        self.computer_figures.append(Rook(7, 7, self.player_side))
        self.computer_figures.append(Knight(7, 1, self.player_side))
        self.computer_figures.append(Knight(7, 6, self.player_side))
        self.computer_figures.append(Bishop(7, 2, self.player_side))
        self.computer_figures.append(Bishop(7, 5, self.player_side))

        if self.computer_side == WHITE:
            self.computer_figures.append(King(7, 3, self.player_side))
            self.computer_figures.append(Queen(7, 4, self.player_side))

        if self.computer_side == BLACK:
            self.computer_figures.append(King(7, 4, self.player_side))
            self.computer_figures.append(Queen(7, 3, self.player_side))

        pass

    # Метод возвращает фигуру, стоящую на клетке r, c
    def get_figure(self, r, c):
        for figure in (self.player_figures + self.computer_figures):
            if figure.row == r and figure.col == c and not figure.is_drop:
                return figure
        return None
