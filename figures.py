import pygame
from params import CELL_SIZE, MOVES, TAKES, DEFENSE


class Figure(pygame.sprite.Sprite):

    def __init__(self, filename, r, c, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(c * CELL_SIZE, r * CELL_SIZE))
        self.row = r
        self.col = c
        self.side = side
        self.is_drop = False

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

    def get_actions(self, board, option):
        result = []

        offsets = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for offset in offsets:
            r1 = self.row + offset[0]
            c1 = self.col + offset[1]
            if not self.is_valid_pos(r1, c1):
                continue
            figure = board.get_figure(r1, c1)
            if figure is None and option == MOVES:
                result.append((r1, c1))
                continue
            if figure is not None:
                if figure.side == self.side and option == DEFENSE:
                    result.append((r1, c1))
                    continue
                if figure.side != self.side and option == TAKES:
                    result.append((r1, c1))
                    continue


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

    # Метод возвращает доступные ходы, взятия или защиты
    def get_actions(self, board, option):
        result = []

        # Ищем только доступные ходы
        if option == MOVES:
            r1 = self.row + self.direction
            c = self.col

            # Проверяем возможность хода на две клетки вперед
            if not self.was_move:
                r2 = self.row + 2 * self.direction
                if board.get_figure(r1, c) is None and board.get_figure(r2, c) is None:
                    result.append((r2, c))

            # Проверяем возможность хода на одну клетку вперед
            if self.is_valid_pos(r1, c):
                if board.get_figure(r1, c) is None:
                    result.append((r1, c))

        # Ищем взятия (за исключением взятия на проходе) и защиты
        if option == TAKES or option == DEFENSE:
            offsets = (-1, 1)
            r1 = self.row + self.direction
            for offset in offsets:
                c1 = self.col + offset
                if not self.is_valid_pos(r1, c1):
                    continue
                figure = board.get_figure(r1, c1)
                if figure is not None:
                    if figure.side == self.side and option == DEFENSE:
                        result.append((r1, c1))
                        continue
                    if figure.side != self.side and option == TAKES:
                        result.append((r1, c1))
                        continue

        # Возвращаем результат
        return result

    # Переопределение метода перемещения необходимо для того, чтобы исключить возможность повторного хода на две клетки
    def set_pos(self, r, c):
        super().set_pos(r, c)
        self.was_move = True
