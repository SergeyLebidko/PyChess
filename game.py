import pygame
from params import FPS, WHITE_CELL_COLOR, BLACK_CELL_COLOR, SELECTED_CELL_COLOR, CELL_SIZE
from board import Board


def start(player_side):
    pygame.init()
    pygame.display.set_caption('PyChess')
    display_surface = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # Выделенная пользователем клетка
    selected_figure = None

    # Создаем текущее игровое поле
    board = Board(player_side)

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_figure = get_mouse_selected_figure(event, board)

        # Блок команд отрисовки
        draw_cells(display_surface)
        draw_select_cell(display_surface, selected_figure)
        draw_figures(display_surface, board)
        pygame.display.update()

        clock.tick(FPS)


# Функция отрисовывает клетки доски
def draw_cells(surface):
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция отрисовывает фигуры на доске
def draw_figures(surface, board):
    for row in range(0, 8):
        for col in range(0, 8):
            figure = board.get_figure(row, col)
            if figure is None:
                continue
            surface.blit(figure.image, figure.rect)


# Функция отрисовывает рамку вокруг выбранной игроком фигуры
def draw_select_cell(surface, selected_figure):
    if selected_figure:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_figure.col * CELL_SIZE, selected_figure.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция определяет клетку, которую выбрал игрок
def get_mouse_selected_cell(mouse_event):
    if mouse_event.button != 1:
        return None
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c


# Функция определяет фигуру, которую выбрал игрок
def get_mouse_selected_figure(mouse_event, board):
    cell = get_mouse_selected_cell(mouse_event)
    if not cell:
        return None
    figure = board.get_figure(cell[0], cell[1])
    return figure
