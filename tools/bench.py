"""Замер скорости работы ИИ на детерминированной партии.

Скрипт не входит в саму игру и запускается только при разработке.
Играет заданное число полуходов и печатает общее, среднее и худшее время
выбора хода, чтобы сравнивать производительность до и после оптимизаций.

Запуск:
    python tools/bench.py          # 14 полуходов по умолчанию
    python tools/bench.py 20       # произвольное число полуходов
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


def main():
    plies = int(sys.argv[1]) if len(sys.argv) > 1 else 14

    board = Board(WHITE)
    ai_white = Ai(WHITE, board)
    ai_black = Ai(BLACK, board)

    total = 0.0
    worst = 0.0
    for ply in range(plies):
        ai = ai_white if ply % 2 == 0 else ai_black
        start = time.time()
        move = ai.get_next_move()
        spent = time.time() - start
        total += spent
        worst = max(worst, spent)
        board.apply_move(move)

    print("plies=%d total=%.3fs avg=%.3fs worst=%.3fs" % (plies, total, total / plies, worst))


if __name__ == "__main__":
    main()
