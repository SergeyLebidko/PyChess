import pygame
from params import CELL_SIZE


class Figure(pygame.sprite.Sprite):

    def __init__(self, filename, r, c):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(c * CELL_SIZE, r * CELL_SIZE))
        self.row = r
        self.col = c

    def set_pos(self, r, c):
        self.row = r
        self.col = c
        self.rect.left = r * CELL_SIZE
        self.rect.top = c * CELL_SIZE


class King(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'King.png', r, c)
        self.side = side


class Queen(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Queen.png', r, c)
        self.side = side


class Rook(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Rook.png', r, c)
        self.side = side


class Bishop(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Bishop.png', r, c)
        self.side = side


class Knight(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Knight.png', r, c)
        self.side = side


class Pawn(Figure):

    def __init__(self, r, c, side):
        Figure.__init__(self, 'sprites/' + side + 'Pawn.png', r, c)
        self.side = side
