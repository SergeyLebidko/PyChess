"""Подсчёт числа листьев дерева ходов (perft) для проверки корректности
генерации ходов.

Скрипт не входит в саму игру и запускается только при разработке.
Используется для контроля того, что оптимизации не меняют множество
генерируемых ходов: значение perft должно совпадать до и после правок.

Запуск:
    python tools/perft.py          # глубины 1..3 по умолчанию
    python tools/perft.py 1 2 3 4  # произвольные глубины
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from game_pack.boards import Board
from game_pack.figures import Queen
from game_pack.params import WHITE, CONVERSION, OPPOSITE_SIDE


def _prepare(move, side, board):
    """Готовит ход к применению (для превращения пешки нужен объект новой
    фигуры, иначе apply_move не сможет его обработать)."""
    if move.m_type == CONVERSION:
        move.new_figure = Queen(move.new_row, move.new_col, side, board)
    return move


def perft(board, side, depth):
    """Число листьев дерева ходов на заданной глубине."""
    moves = board.get_all_avl_moves(side)
    if depth == 1:
        return len(moves)

    total = 0
    op_side = OPPOSITE_SIDE[side]
    for move in moves:
        _prepare(move, side, board)
        board.apply_move(move)
        total += perft(board, op_side, depth - 1)
        board.cancel_move()
    return total


def main():
    depths = [int(x) for x in sys.argv[1:]] or [1, 2, 3]
    board = Board(WHITE)
    for depth in depths:
        start = time.time()
        nodes = perft(board, WHITE, depth)
        print("perft(%d) = %d  (%.3fs)" % (depth, nodes, time.time() - start))


if __name__ == "__main__":
    main()
