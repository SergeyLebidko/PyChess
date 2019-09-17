import pygame
from params import *
from board import Board


def start(player_side):
    pygame.init()
    pygame.display.set_caption('PyChess')
    display_surface = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # Выделенная пользователем клетка
    selected_cell = ()

    # Список фигур на доске
    board = Board(player_side)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = mouse_handler(event)

        draw_cells(display_surface)
        draw_select_frame(display_surface, selected_cell)
        draw_figures(display_surface, board)
        pygame.display.update()

        clock.tick(FPS)


def draw_cells(surface):
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_select_frame(surface, selected_cell):
    if selected_cell:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)


def draw_figures(surface, board):
    for row in range(0, 8):
        for col in range(0, 8):
            figure = board.get_figure(row, col)
            if figure is None:
                continue
            surface.blit(figure.image, figure.rect)


def mouse_handler(mouse_event):
    if mouse_event.button != 1:
        return
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c
