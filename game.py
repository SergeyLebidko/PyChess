import pygame
from params import *
from figures import Queen


def start():
    pygame.init()
    pygame.display.set_caption('PyChess')
    display_surface = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # Выделенная пользователем клетка
    selected_cell = ()

    # Список фигур на доске
    figures = []

    # Тестовый код
    figures.append(Queen(3, 0))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = mouse_handler(event)

                # Тестовый код
                figures[-1].set_pos(selected_cell[1], selected_cell[0])

        draw_board(display_surface)
        draw_selected_cell(display_surface, selected_cell)
        draw_figures(display_surface, selected_cell)
        pygame.display.update()

        clock.tick(FPS)


def draw_board(surface):
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_selected_cell(surface, selected_cell):
    if selected_cell:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)


def draw_figures(surface, figures):
    for figure in figures:
        surface.blit(figure.image, figure.rect)


def mouse_handler(mouse_event):
    if mouse_event.button != 1:
        return
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c
