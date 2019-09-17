import pygame
from params import CELL_SIZE


class Figure(pygame.sprite.Sprite):

    def __init__(self, filename, r, c, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(c * CELL_SIZE, r * CELL_SIZE))
        self.row = r
        self.col = c
        self.side = side

    def set_pos(self, r, c):
        self.row = r
        self.col = c
        self.rect.left = r * CELL_SIZE
        self.rect.top = c * CELL_SIZE


class King(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'King.png', r, c, side)


class Queen(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Queen.png', r, c, side)


class Rook(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Rook.png', r, c, side)


class Bishop(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Bishop.png', r, c, side)


class Knight(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Knight.png', r, c, side)


class Pawn(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Pawn.png', r, c, side)

        # Выбираем направление движения пешки в зависимости от того, кому она принадлежит - игроку или компьютеру
        if self.col == 1:
            self.direction = 1
        if self.row == 6:
            self.direction = -1

        # Флаг равен True, если пешка уже делала ход
        self.was_move = False

    # Метод возвращает список клеток, на которые может пойти пешка
    def get_moves(self, board):
        pass

    # Метод возвращает список взятий, которые может совершить пешка
    def get_takes(self, board):
        pass
