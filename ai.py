import random
from figures import *


class Ai:

    def __init__(self, side, board):
        self.side = side
        self.board = board

    # Метод возвращает следующий ход компьютера
    def get_next_move(self):
        # Получаем список доступных ходов
        avl_moves = self.board.get_all_avl_moves(self.side)

        # Если это первый ход в игре, то выбираем его случайным образом
        if self.board.get_moves_count() == 0:
            random.seed()
            move = avl_moves[random.randint(0, len(avl_moves) - 1)]
            return move

        # Иначе нам нужно выбрать ход с максимальной оценкой
        rating = 0
        max_rating = -1000000
        move_with_max_rating = None
        for move in avl_moves:
            self.board.apply_move(move)
            rating = self.get_rating(self.side, 2)
            self.board.cancel_move()
            if rating > max_rating:
                max_rating = rating
                move_with_max_rating = move

        # Возвращаем найденный ход
        return move_with_max_rating

    # Метод возвращает оценку хода. d - глубина рекурсии
    def get_rating(self, side, d):
        if d == 0:
            # Получем оценку для примененного хода
            evaluate = self.board.position_evaluation(side)

            # Возвращаем результат
            return evaluate

        rating = 0
        max_rating = -1000000
        avl_moves = self.board.get_all_avl_moves(OPPOSITE_SIDE[side])
        for avl_move in avl_moves:
            self.board.apply_move(avl_move)
            rating = (-1) * self.get_rating(OPPOSITE_SIDE[side], d - 1)
            self.board.cancel_move()
            if rating > max_rating:
                max_rating = rating

        # Возвращаем результат
        return max_rating
