from boards import *
from params import *
from ai import *

# Текущий холст
surface = None

# Текущее игровое поле
board = None

# Выделенная пользователем фигура
selected_figure = None

# Список доступных ходов
avl_moves = []

# Выбранный ход
selected_move = None

# Сообщение
msg = None


def start(player_side):
    global surface, board, selected_figure, avl_moves, selected_move, mode, msg
    pygame.init()
    pygame.display.set_caption('PyChess')
    surface = pygame.display.set_mode((CELL_SIZE * 8, CELL_SIZE * 8))
    clock = pygame.time.Clock()

    # Определяем фигруры (белые или черные), которыми будем играть компьютер
    computer_side = OPPOSITE_SIDE[player_side]

    # Если компьютер играет белыми, то его ход должен быть первым, иначе - первым ходит игрок
    if computer_side == WHITE:
        mode = 'mode_5'
    else:
        mode = 'mode_1'

    # Создаем игровое поле
    main_board = Board(player_side)
    board = main_board

    # Создаем объект, отвечающий за расчет ответного хода
    ai = Ai(computer_side, main_board)

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    # Тестовый код отката хода при нажатии на любую кнопку мыши, кроме левой
                    board.cancel_move()
                    continue

                # В режиме 1 разрешен только выбор фигур
                #  При выборе фигуры, получаем список доступных ходов для неё и если он не пуст - переходим в режим 2
                if mode == 'mode_1':
                    selected_figure = get_mouse_selected_figure(event, player_side)
                    if selected_figure is not None:
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                        if avl_moves:
                            mode = 'mode_2'
                            continue

                # В режиме 2 разрешен выбор фигур и ходов
                # Если выбран ход-конверсия, то переходим в режим 3
                # Если выбран любой другой ход, то переходим в режим 4
                # Если выбрана другая фигура, то получаем её список доступных ходов
                if mode == 'mode_2':
                    selected_row, selected_col = get_mouse_selected_cell(event)
                    # Сперва проверяем, выбран ли ход
                    selected_move = None
                    for move in avl_moves:
                        if selected_row == move.new_row and selected_col == move.new_col:
                            selected_move = move
                            break

                    if selected_move is not None:
                        # Если ход выбран и это ход-конверсия, то переходим в режим 3
                        if selected_move.m_type == CONVERSION:
                            selected_figure = None
                            avl_moves = []
                            board = SelectorBoard(player_side, main_board)
                            mode = 'mode_3'
                            continue
                        # Если ход выбран и это не ход-конверсия, то переходим в режим 4
                        mode = 'mode_4'
                        continue

                    # Если выбрана фигура, то получаем ее список доступных ходов
                    new_selected_figure = get_mouse_selected_figure(event, player_side)
                    if new_selected_figure is not None:
                        selected_figure = new_selected_figure
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                    continue

                # В режиме 3  нужно выбрать фигуру для хода конверсии
                # Если фигруа выбрана, то записываем её в объект хода и переходим в режим 4
                if mode == 'mode_3':
                    selected_figure = get_mouse_selected_figure(event, player_side)
                    if selected_figure is not None:
                        selected_figure.set_pos(selected_move.new_row, selected_move.new_col)
                        selected_move.new_figure = selected_figure
                        board = main_board
                        mode = 'mode_4'
                        continue

                # В режиме шесть игроку выведено сообщение о завершении игры и любой щелчок мышью приводит к выходу
                if mode == 'mode_6':
                    exit()

        # Режим 4 не связан с событиями мыши ил клавиатуры
        # В этом режиме происходит процесс применения хода игрока и проверка условия завешения игры
        if mode == 'mode_4':
            board.apply_move(selected_move)
            selected_figure = None
            selected_move = None
            avl_moves = []
            # Вставить код проверки завершения игры
            # Если игра завершена, то перейти в режим 6
            # Если игра не завершена, то перейти в режим 5
            mode = 'mode_5'

        # В режиме 5 происходит вычисление ответного хода компьютера и проверка его результатов
        # Если игра завершена, то происходит переход в режим 6
        # Если игра не завершена, то происходит переход в режим 1
        if mode == 'mode_5':
            move = ai.get_next_move()
            board.apply_move(move)
            selected_figure = None
            selected_move = None
            avl_moves = []
            # Вставить код проверки завершения игры
            # Если игра завершена, то перейти в режим 6
            # Если игра не завершена, то перейтив режим 1
            mode = 'mode_1'

        # Блок команд отрисовки
        draw_cells()
        draw_select_cell()
        draw_avl_moves()
        draw_figures()
        draw_msg()
        pygame.display.update()

        clock.tick(FPS)


# Функция отрисовывает клетки доски
def draw_cells():
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция отрисовывает фигуры на доске
def draw_figures():
    for row in range(0, 8):
        for col in range(0, 8):
            figure = board.get_figure(row, col)
            if figure is None:
                continue
            surface.blit(figure.image, figure.rect)


# Функция отрисовывает выбранную игроком клетку
def draw_select_cell():
    if selected_figure:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_figure.col * CELL_SIZE, selected_figure.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция отрисовывает клетки, доступные для хода выбранной фигурой
def draw_avl_moves():
    for move in avl_moves:
        row_move = move.new_row
        col_move = move.new_col
        pygame.draw.rect(surface, AVL_MOVE_CELL_COLOR,
                         (col_move * CELL_SIZE + 4, row_move * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))
    pass


# Функция отрисовки сообщения
def draw_msg():
    if not msg:
        return
    font = pygame.font.Font(None, 56)
    msg_surface = font.render(msg, 1, MSG_COLOR)
    x_pos = CELL_SIZE * 4 - msg_surface.get_width() // 2
    y_pos = CELL_SIZE * 4 - msg_surface.get_height() // 2
    msg_rect = msg_surface.get_rect(topleft=(x_pos, y_pos))

    surface.blit(msg_surface, msg_rect)


# Функция определяет клетку, которую выбрал игрок
def get_mouse_selected_cell(mouse_event):
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c


# Функция определяет фигуру, которую выбрал игрок
def get_mouse_selected_figure(mouse_event, side=None):
    selected_row, selected_col = get_mouse_selected_cell(mouse_event)
    figure = board.get_figure(selected_row, selected_col)
    if side is not None and figure is not None:
        if figure.side != side:
            return None
    return figure
