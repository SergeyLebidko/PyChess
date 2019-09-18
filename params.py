# Частота кадро
FPS = 30

# Константы сторон
WHITE = 'white'
BLACK = 'black'

# Ширина/высота клетки в пикселях
CELL_SIZE = 50

# Цвета для белых и черных клеток
WHITE_CELL_COLOR = (230, 230, 230)
BLACK_CELL_COLOR = (150, 150, 150)

# Цвет выделенной ячейки
SELECTED_CELL_COLOR = (100, 100, 255)

# Опции для получения списков ходов
MOVES = 'moves'                         # Обычные ходы
TAKES = 'takes'                         # Взятия
DEFENSE = 'defence'                     # Защиты

# Типы ходов
NORMAL_MOVE = 'normal_move'             # Обычный ход
TAKE_MOVE = 'take_move'                 # Ход-взятие
CASTLING = 'castling'                   # Рокировка
CONVERSION = 'conversion'               # Превращение пешки в другую фигуру
PASSED_TAKE = 'passed_take'             # Взятие на проходе
