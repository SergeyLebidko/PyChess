import random


class Ai:

    def __init__(self, side, board):
        self.side = side
        self.board = board

    # Метод возвращает следующий ход компьютера
    def get_next_move(self):
        # Временный код-заглушка, необходимый для тестирования. В дальнейшем будет удален
        random.seed()
        avl_moves = self.board.get_all_avl_moves(self.side)
        move = avl_moves[random.randint(0, len(avl_moves)-1)]
        return move
