# Частота кадров
FPS = 5

# Константы сторон
WHITE = 'white'
BLACK = 'black'

# Словарь для быстрого определения противоположной стороны
OPPOSITE_SIDE = {WHITE: BLACK, BLACK: WHITE}

# Ширина/высота клетки в пикселях
CELL_SIZE = 72

# Цвета для белых и черных клеток
WHITE_CELL_COLOR = (230, 230, 230)
BLACK_CELL_COLOR = (150, 150, 150)

# Цвет текста для сообщений
MSG_COLOR = (255, 10, 10)

# Оформление плашки "Компьютер думает"
THINKING_PLATE_BG_COLOR = (255, 255, 255)      # Фон плашки
THINKING_PLATE_BORDER_COLOR = (0, 0, 0)        # Цвет границы плашки
THINKING_TEXT_COLOR = (0, 0, 0)                # Цвет текста на плашке
THINKING_PLATE_BORDER_WIDTH = 3                # Толщина границы плашки
THINKING_PLATE_PADDING = 16                    # Отступ текста от краев плашки
THINKING_PLATE_EXTRA_WIDTH = 20                # Дополнительная ширина плашки
THINKING_PLATE_RADIUS = 10                     # Радиус скругления углов плашки

# Цвет выделенной ячейки
SELECTED_CELL_COLOR = (120, 120, 255)

# Цвет клетки короля игрока, если он под шахом
KING_ON_SHAH_COLOR = (255, 0, 0)

# Цвет ячейки, доступной для хода
AVL_MOVE_CELL_COLOR = (255, 120, 120)

# Имена действий, доступных для пешки
PAWN_MOVES = 'pawn_moves'
PAWN_TAKES = 'pawn_takes'

# Типы ходов
NORMAL_MOVE = 'normal_move'  # Обычный ход
TAKE_MOVE = 'take_move'      # Ход-взятие
CASTLING = 'castling'        # Рокировка
CONVERSION = 'conversion'    # Превращение пешки в другую фигуру
PASSED_TAKE = 'passed_take'  # Взятие на проходе

# Приоритеты ходов: чем меньше ранг, тем раньше рассматривается ход.
# Ранние ходы-взятия быстрее приводят к значимым изменениям на доске и
# ускоряют отсечение заведомо неудачных позиций при поиске.
_move_type_rank = {
    TAKE_MOVE: 0,
    CONVERSION: 1,
    PASSED_TAKE: 2,
    CASTLING: 3,
    NORMAL_MOVE: 4,
}

# Ценность фигур, используемая при сортировке взятий (MVV-LVA):
# в первую очередь выгодно брать более ценную фигуру, желательно менее
# ценной фигурой.
_move_value_by_name = {
    'Pawn': 100,
    'Knight': 300,
    'Bishop': 300,
    'Rook': 500,
    'Queen': 900,
    'King': 9000,
}


# Функция-ключ для сортировки ходов
def key_func_for_moves(move):
    rank = _move_type_rank.get(move.m_type, len(_move_type_rank))

    # Для взятий дополнительно учитываем "ценность жертвы минус ценность
    # атакующего": такие ходы оказываются впереди и ускоряют отсечение.
    if move.m_type in (TAKE_MOVE, PASSED_TAKE):
        victim = getattr(move, 'drop_figure', None)
        victim_value = _move_value_by_name.get(type(victim).__name__, 0) if victim is not None else 0
        attacker_value = _move_value_by_name.get(type(move.figure).__name__, 0)
        return rank, -(victim_value - attacker_value)

    return rank, 0


# Варианты завершения игры
MAT = 'mat'  # Игра завершилась матом
PAT = 'pat'  # Игра завершилась патом

# Настройки поиска хода компьютером
# Бюджет времени на один ход (в секундах) для итеративного углубления
AI_TIME_BUDGET = 1.8
# Максимальная глубина поиска (верхняя граница для итеративного углубления)
AI_MAX_DEPTH = 12

# Настройки анимации ходов
# Длительность анимации одного хода (в секундах)
ANIM_DURATION = 0.18
# Частота кадров во время анимации хода
ANIM_FPS = 60

# Пауза перед первым ходом компьютера (в секундах), если он играет белыми.
# Позволяет игроку увидеть начальную позицию перед ответом компьютера.
AI_FIRST_MOVE_DELAY = 0.25
