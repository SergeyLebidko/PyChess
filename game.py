import pygame
from params import *
from boards import Board


def start(player_side):
    pygame.init()
    pygame.display.set_caption('PyChess')
    display_surface = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # Выделенная пользователем клетка
    selected_figure = None

    # Список доступных ходов
    avl_moves = []

    # Создаем текущее игровое поле
    board = Board(player_side)

    # Текущий режим работы
    mode = 'mode_1'

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue

                if mode == 'mode_1':
                    # В первом режиме разрешен выбор только фигур
                    selected_figure = get_mouse_selected_figure(event, board)
                    if selected_figure is not None:
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                        mode = 'mode_2'
                    continue
                if mode == 'mode_2':
                    # Во втором режиме можно выбирать и фигуры, и клетки, доступные для хода
                    selected_row, selected_col = get_mouse_selected_cell(event)

                    # Проверяем, был ли выбран доступный ход и, если да, то применяем его
                    applied_move = None
                    for move in avl_moves:
                        if move.new_row == selected_row and move.new_col == selected_col:
                            applied_move = move
                            break
                    if applied_move is not None:
                        board.apply_move(applied_move)
                        selected_figure = None
                        avl_moves = []
                        mode = 'mode_1'
                        continue

                    # Если была выбрана другая фигура, то получаем список ходов для неё
                    new_selected_figure = get_mouse_selected_figure(event, board)
                    if new_selected_figure is not None:
                        if selected_figure != new_selected_figure:
                            selected_figure = new_selected_figure
                            avl_moves = board.get_avl_moves_for_figure(selected_figure)

        # Блок команд отрисовки
        draw_cells(display_surface)
        draw_select_cell(display_surface, selected_figure)
        draw_avl_moves(display_surface, avl_moves)
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


# Функция отрисовывает выбранную игроком клетку
def draw_select_cell(surface, selected_figure):
    if selected_figure:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_figure.col * CELL_SIZE, selected_figure.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция отрисовывает клетки, доступные для хода выбранной фигурой
def draw_avl_moves(surface, avl_moves):
    for move in avl_moves:
        row_move = move.new_row
        col_move = move.new_col
        pygame.draw.rect(surface, AVL_MOVE_CELL_COLOR,
                         (col_move * CELL_SIZE + 4, row_move * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))
    pass


# Функция определяет клетку, которую выбрал игрок
def get_mouse_selected_cell(mouse_event):
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c


# Функция определяет фигуру, которую выбрал игрок
def get_mouse_selected_figure(mouse_event, board, side=None):
    cell = get_mouse_selected_cell(mouse_event)
    figure = board.get_figure(cell[0], cell[1])
    if side is not None and figure is not None:
        if figure.side != side:
            return None
    return figure
