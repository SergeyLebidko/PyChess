from game_pack.boards import *
from game_pack.ai import *

import queue
import threading
import time

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

# Равен True, если король игрока находится под шахом
shah_flag = False

# Сообщение
msg = None

# Поток расчета хода компьютера и очередь для передачи результата
ai_thread = None
ai_result_queue = None

# Снимок доски, отображаемый пока компьютер думает
thinking_surface = None

# Состояние анимации хода
# Список движущихся фигур: (image, start_x, start_y, end_x, end_y)
anim_pieces = []
# Фигуры, которые нужно пропустить при обычной отрисовке во время анимации
anim_hidden = set()
# Момент начала текущей анимации
anim_start = 0.0
# Отложенное состояние, применяемое после завершения анимации
pending_mode = None
pending_msg = None

# Момент времени, до которого нужно выдержать паузу перед первым ходом
# компьютера (используется, когда компьютер играет белыми). None - паузы нет.
ai_delay_until = None


def start(player_side):
    global surface, board, selected_figure, avl_moves, selected_move, mode, shah_flag, msg
    global ai_thread, ai_result_queue, thinking_surface
    global anim_pieces, anim_hidden, anim_start, pending_mode, pending_msg
    global ai_delay_until
    pygame.init()
    pygame.display.set_caption('PyChess')
    surface = pygame.display.set_mode((CELL_SIZE * 8, CELL_SIZE * 8))
    clock = pygame.time.Clock()

    # Определяем фигруры (белые или черные), которыми будем играть компьютер
    computer_side = OPPOSITE_SIDE[player_side]

    # Если компьютер играет белыми, то его ход должен быть первым, иначе - первым ходит игрок.
    # Перед первым ходом компьютера выдерживаем небольшую паузу, чтобы игрок успел
    # увидеть начальную позицию.
    if computer_side == WHITE:
        mode = 'mode_5'
        ai_delay_until = time.time() + AI_FIRST_MOVE_DELAY
    else:
        mode = 'mode_1'
        ai_delay_until = None

    # Создаем игровое поле
    main_board = Board(player_side)
    board = main_board

    # Создаем объект, отвечающий за расчет ответного хода
    ai = Ai(computer_side, main_board)

    # Поток расчета хода компьютера и очередь результата (создаются по мере надобности)
    ai_thread = None
    ai_result_queue = None
    thinking_surface = None

    # Состояние анимации ходов
    anim_pieces = []
    anim_hidden = set()
    anim_start = 0.0
    pending_mode = None
    pending_msg = None

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
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

        # Режим 4 не связан с событиями мыши или клавиатуры
        # В этом режиме происходит процесс применения хода игрока и проверка условия завешения игры
        if mode == 'mode_4':
            board.apply_move(selected_move)

            # Сбрасываем флаг шаха игроку. Это можно делать, так как ходы игрока, которые приводили бы
            # к шаху ему же самому - запрещены и отсекаются фильтром ходов в board
            shah_flag = False

            # Код проверки завершения игры
            game_over = check_game_over(computer_side)
            if game_over == MAT:
                next_mode, next_msg = 'mode_6', 'Вы победили!'
            elif game_over == PAT:
                next_mode, next_msg = 'mode_6', 'Ничья'
            else:
                next_mode, next_msg = 'mode_5', None

            # Запускаем анимацию хода игрока
            begin_animation(selected_move, next_mode, next_msg)
            selected_figure = None
            selected_move = None
            avl_moves = []
            continue

        # В режиме 5 происходит вычисление ответного хода компьютера.
        # Расчет ведется в отдельном потоке, чтобы окно не переставало
        # отвечать на события. Пока поток работает, отображается снимок
        # доски и индикатор "Компьютер думает...".
        if mode == 'mode_5':
            # Если задана пауза перед первым ходом компьютера - ждём её окончания,
            # продолжая отрисовывать доску и обрабатывать события
            if ai_delay_until is not None:
                if time.time() < ai_delay_until:
                    repaint()
                    clock.tick(FPS)
                    continue
                ai_delay_until = None

            # Если поток еще не запущен - запускаем расчет хода
            if ai_thread is None:
                # Отрисовываем актуальное состояние доски и запоминаем снимок
                # для показа, пока компьютер думает
                repaint()
                thinking_surface = surface.copy()
                ai_result_queue = queue.Queue()
                ai_thread = threading.Thread(
                    target=_calculate_move, args=(ai, ai_result_queue), daemon=True)
                ai_thread.start()

            # Пока поток считает - отображаем снимок и индикатор, продолжая
            # обрабатывать события (окно остается отзывчивым)
            if ai_thread.is_alive():
                draw_thinking(thinking_surface)
                clock.tick(FPS)
                continue

            # Поток завершился: забираем результат и применяем ход
            move = ai_result_queue.get()
            ai_thread = None
            ai_result_queue = None
            thinking_surface = None

            # Если в потоке произошла ошибка - сообщаем о ней и завершаем партию
            if isinstance(move, BaseException):
                raise move

            board.apply_move(move)

            # Проверяем, установлен ли шах королю игрока
            if board.is_strike_figure(board.pl_king):
                shah_flag = True

            # Код проверки завершения игры
            game_over = check_game_over(player_side)
            if game_over == MAT:
                next_mode, next_msg = 'mode_6', 'Вы проиграли...'
            elif game_over == PAT:
                next_mode, next_msg = 'mode_6', 'Ничья'
            else:
                next_mode, next_msg = 'mode_1', None

            # Запускаем анимацию хода компьютера
            begin_animation(move, next_mode, next_msg)
            selected_figure = None
            selected_move = None
            avl_moves = []
            continue

        # В режиме анимации проигрывается плавное перемещение фигур.
        # По завершении применяется отложенное состояние (режим и сообщение).
        if mode == 'mode_anim':
            elapsed = time.time() - anim_start
            progress = elapsed / ANIM_DURATION
            if progress >= 1.0:
                # Анимация завершена - применяем отложенное состояние
                anim_pieces = []
                anim_hidden = set()
                mode = pending_mode
                msg = pending_msg
                continue

            repaint(progress)
            clock.tick(ANIM_FPS)
            continue

        repaint()
        clock.tick(FPS)


# Функция подготавливает анимацию хода и переводит игру в режим анимации.
# move - применённый ход; next_mode/next_msg описывают состояние после хода
def begin_animation(move, next_mode, next_msg):
    global anim_pieces, anim_hidden, anim_start, pending_mode, pending_msg, mode

    anim_pieces = []
    anim_hidden = set()

    # Обычный ход, взятие или взятие на проходе: едет одна фигура
    if move.m_type in (NORMAL_MOVE, TAKE_MOVE, PASSED_TAKE):
        _add_anim_piece(move.figure, move.old_row, move.old_col, move.new_row, move.new_col)
        anim_hidden = {move.figure}

    # Рокировка: синхронно едут король и ладья
    elif move.m_type == CASTLING:
        _add_anim_piece(move.figure, move.old_row, move.old_col, move.new_row, move.new_col)
        _add_anim_piece(move.rook, move.old_row_rook, move.old_col_rook, move.new_row_rook, move.new_col_rook)
        anim_hidden = {move.figure, move.rook}

    # Превращение пешки: пешка "доезжает" до клетки, новая фигура проявляется после
    elif move.m_type == CONVERSION:
        _add_anim_piece(move.figure, move.old_row, move.old_col, move.new_row, move.new_col)
        anim_hidden = {move.figure}
        if move.new_figure is not None:
            anim_hidden.add(move.new_figure)

    anim_start = time.time()
    pending_mode = next_mode
    pending_msg = next_msg
    mode = 'mode_anim'


# Функция регистрирует движущуюся фигуру (координаты в пикселях)
def _add_anim_piece(figure, old_row, old_col, new_row, new_col):
    anim_pieces.append((
        figure.image,
        old_col * CELL_SIZE,
        old_row * CELL_SIZE,
        new_col * CELL_SIZE,
        new_row * CELL_SIZE,
    ))


# Функция отрисовывает движущиеся фигуры в интерполированной позиции
def draw_moving_pieces(progress):
    # Сглаживание ease-out: движение быстро начинается и плавно замедляется
    k = 1.0 - (1.0 - progress) ** 2
    for image, start_x, start_y, end_x, end_y in anim_pieces:
        x = start_x + (end_x - start_x) * k
        y = start_y + (end_y - start_y) * k
        surface.blit(image, (int(x), int(y)))


# Функция выполняется в отдельном потоке: считает ход и кладет его в очередь
def _calculate_move(ai, result_queue):
    try:
        result_queue.put(ai.get_next_move())
    except BaseException as error:
        # Передаем ошибку в главный поток, чтобы не оставить окно в ожидании
        result_queue.put(error)


# Функция отрисовывает снимок доски и плашку "Компьютер думает"
def draw_thinking(snapshot):
    surface.blit(snapshot, (0, 0))

    # Рендерим текст индикатора
    font = pygame.font.Font(None, 40)
    text_surface = font.render('Компьютер думает', True, THINKING_TEXT_COLOR)

    # Размер плашки = размер текста плюс отступы со всех сторон.
    # Ширина дополнительно увеличена, чтобы границы плашки не совпадали
    # с границами клеток доски.
    plate_width = text_surface.get_width() + THINKING_PLATE_PADDING * 2 + THINKING_PLATE_EXTRA_WIDTH
    plate_height = text_surface.get_height() + THINKING_PLATE_PADDING * 2

    # Центрируем плашку относительно центра доски
    plate_x = CELL_SIZE * 4 - plate_width // 2
    plate_y = CELL_SIZE * 4 - plate_height // 2
    plate_rect = pygame.Rect(plate_x, plate_y, plate_width, plate_height)

    # Рисуем плашку: заливка, затем граница
    pygame.draw.rect(surface, THINKING_PLATE_BG_COLOR, plate_rect,
                     border_radius=THINKING_PLATE_RADIUS)
    pygame.draw.rect(surface, THINKING_PLATE_BORDER_COLOR, plate_rect,
                     width=THINKING_PLATE_BORDER_WIDTH, border_radius=THINKING_PLATE_RADIUS)

    # Рисуем текст по центру плашки
    text_rect = text_surface.get_rect(center=plate_rect.center)
    surface.blit(text_surface, text_rect)

    pygame.display.update()


# Функция проверяет, завершалась ли игра для данной стороны
def check_game_over(side):
    king = board.kings_dict[side]
    sh_flag = board.is_strike_figure(king)
    avl_flag = (len(board.get_all_avl_moves(side)) == 0)
    if avl_flag and sh_flag:
        return MAT
    if avl_flag and not sh_flag:
        return PAT
    return None


# Функция выполняет команды отрисовки
def repaint(anim_progress=None):
    # Блок команд отрисовки
    draw_cells()
    draw_select_cell()
    draw_avl_moves()
    draw_shah_cell()
    draw_figures()
    if anim_progress is not None:
        draw_moving_pieces(anim_progress)
    draw_msg()
    pygame.display.update()


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
            # Во время анимации движущиеся фигуры рисуются отдельно
            if figure in anim_hidden:
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


# Функция отрисовывает клетку короля игрока, если он находится под шахом
def draw_shah_cell():
    if shah_flag:
        row = board.pl_king.row
        col = board.pl_king.col
        pygame.draw.rect(surface, KING_ON_SHAH_COLOR,
                         (col * CELL_SIZE + 4, row * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))


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
