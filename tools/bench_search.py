"""Замер скорости поиска на фиксированных позициях (без влияния выбора хода).

Скрипт не входит в игру и запускается при разработке. В отличие от bench.py,
здесь ИИ не выбирает ход для игры, а лишь считает оценку дерева на заданную
глубину из заранее построенных позиций. Это делает замер детерминированным и
позволяет честно сравнивать скорость поиска до и после оптимизаций (в том
числе изменений порядка ходов).

Запуск:
    python tools/bench_search.py
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

from game_pack.ai import Ai
from game_pack.boards import Board
from game_pack.params import BLACK, WHITE


# Небольшая детерминированная дебютная последовательность.
# Каждый элемент: (строка-откуда, столбец-откуда, строка-куда, столбец-куда).
OPENING = [
    (6, 4, 4, 4),  # 1. e4
    (1, 4, 3, 4),  # 1... e5
    (7, 6, 5, 5),  # 2. Nf3
    (0, 1, 2, 2),  # 2... Nc6
    (7, 5, 3, 1),  # 3. Bb5
    (1, 0, 2, 0),  # 3... a6
    (3, 1, 4, 2),  # 4. Ba4
    (0, 6, 2, 5),  # 4... Nf6
]


def find_move(board, side, from_row, from_col, to_row, to_col):
    for move in board.get_all_avl_moves(side):
        if (move.figure.row == from_row and move.figure.col == from_col
                and move.new_row == to_row and move.new_col == to_col):
            return move
    raise RuntimeError("move not found: %s" % ((from_row, from_col, to_row, to_col),))


def build_position():
    board = Board(WHITE)
    ai_white = Ai(WHITE, board)
    ai_black = Ai(BLACK, board)
    return board, ai_white, ai_black


def search_time(board, side, depth):
    ai = Ai(side, board)
    start = time.time()
    ai.search(depth)
    return time.time() - start


def main():
    board, _, _ = build_position()

    # Позиция A: начальная
    positions = [(board, WHITE, "start")]

    # Продвигаемся по дебютной последовательности, снимая замеры
    side = WHITE
    for i, (fr, fc, tr, tc) in enumerate(OPENING):
        move = find_move(board, side, fr, fc, tr, tc)
        board.apply_move(move)
        side = BLACK if side == WHITE else WHITE
    positions.append((board, WHITE, "after opening"))

    total = 0.0
    for pos_board, pos_side, name in positions:
        for depth in (2, 3):
            spent = search_time(pos_board, pos_side, depth)
            total += spent
            print("position=%-14s side=%-5s depth=%d  %.3fs" % (name, pos_side, depth, spent))
    print("TOTAL=%.3fs" % total)
    return total


if __name__ == "__main__":
    main()
