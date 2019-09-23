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
            rating = self.get_rating(move)
            if rating > max_rating:
                max_rating = rating
                move_with_max_rating = move

        # Возвращаем найденный ход
        print()
        return move_with_max_rating

    def get_rating(self, move):
        # Применяем переданный ход
        self.board.apply_move(move)

        # Получем оценку для примененного хода
        eval = self.board.position_evaluation(move.figure.side)

        # Откатываем примененный ход
        self.board.cancel_move()

        # Возвращаем результат
        print(eval)
        return eval
