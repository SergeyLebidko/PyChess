# Частота кадров
FPS = 5

# Константы сторон
WHITE = 'white'
BLACK = 'black'

# Ширина/высота клетки в пикселях
CELL_SIZE = 50

# Цвета для белых и черных клеток
WHITE_CELL_COLOR = (230, 230, 230)
BLACK_CELL_COLOR = (150, 150, 150)

# Цвет текста для сообщений
MSG_COLOR = (30, 30, 160)

# Цвет выделенной ячейки
SELECTED_CELL_COLOR = (120, 120, 255)

# Цвет ячейки, доступной для хода
AVL_MOVE_CELL_COLOR = (255, 120, 120)

# Имена действий, доступных для пешки
PAWN_MOVES = 'pawn_moves'
PAWN_TAKES = 'pawn_takes'

# Типы ходов
NORMAL_MOVE = 'normal_move'   # Обычный ход
TAKE_MOVE = 'take_move'       # Ход-взятие
CASTLING = 'castling'         # Рокировка
CONVERSION = 'conversion'     # Превращение пешки в другую фигуру
PASSED_TAKE = 'passed_take'   # Взятие на проходе
