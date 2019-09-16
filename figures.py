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


class Queen(Figure):

    def __init__(self, r, c):
        Figure.__init__(self, 'sprites/whiteQueen.png', r, c)
