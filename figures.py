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

    @staticmethod
    def is_valid_pos(r, c):
        if 0 <= r <= 7 and 0 <= c <= 7:
            return True
        else:
            return False


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
        moves = []

        # Проверяем возможность хода на две клетки вперед
        if not self.was_move:
            if board.get_figure(self.row + self.direction, self.col) is None:
                if board.get_figure(self.row + 2 * self.direction, self.col) is None:
                    moves.append((self.row + 2 * self.direction, self.col))

        # Проверяем возможность хода на одну клетку вперед
        if board.get_figure(self.row + self.direction, self.col) is None:
            moves.append((self.row + self.direction, self.col))

        # Возвращаем результат
        return moves

    # Метод возвращает список взятий, которые может совершить пешка (исключая взятия на проходе)
    def get_takes(self, board):
        takes = []

        r1 = self.row + self.direction
        c1 = self.col - 1
        r2 = self.row + self.direction
        c2 = self.col + 1

        # Проверяем взятие влево
        if self.is_valid_pos(r1, c1):
            figure = board.get_figure(r1, c1)
            if figure is not None:
                if figure.side != self.side:
                    takes.append((r1, c1))

        # Проверяем взятие вправо
        if self.is_valid_pos(r2, c2):
            figure = board.get_figure(r2, c2)
            if figure is not None:
                if figure.side != self.side:
                    takes.append((r2, c2))

        # Возвращаем результат
        return takes

    # Переопределение метода перемещения необходимо для того, чтобы исключить возможность повторного хода на две клетки
    def set_pos(self, r, c):
        super().set_pos(r, c)
        self.was_move = True
