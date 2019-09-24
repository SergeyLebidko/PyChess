from figures import *


class Move:

    def __init__(self, move_type, figure, new_row, new_col):
        self.m_type = move_type
        self.figure = figure
        self.new_row = new_row
        self.new_col = new_col
        self.old_row = figure.row
        self.old_col = figure.col


class Board:

    def __init__(self, pl_side):
        self.pl_side = pl_side
        self.cmp_side = OPPOSITE_SIDE[pl_side]

        # Списки фигур игрока и компьютера
        self.pl_figures = []
        self.cmp_figures = []

        # Словарь, позволяющий быстро найти список фигур по их цвету
        self.figures_dict = {self.pl_side: self.pl_figures, self.cmp_side: self.cmp_figures}

        # Словарь, позволяющий быстро найти короля по его цвету
        self.kings_dict = {}

        # Создаем фигуры компьютера
        if self.cmp_side == WHITE:
            self.cmp_king = King(0, 3, self.cmp_side, self)
            self.kings_dict[WHITE] = self.cmp_king
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 4, self.cmp_side, self))

        if self.cmp_side == BLACK:
            self.cmp_king = King(0, 4, self.cmp_side, self)
            self.kings_dict[BLACK] = self.cmp_king
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 3, self.cmp_side, self))

        self.cmp_figures.append(Rook(0, 0, self.cmp_side, self))
        self.cmp_figures.append(Rook(0, 7, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 1, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 6, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 2, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 5, self.cmp_side, self))

        for i in range(0, 8):
            self.cmp_figures.append(Pawn(1, i, self.cmp_side, self))

        # Создаем фигуры игрока
        if self.pl_side == BLACK:
            self.pl_king = King(7, 3, self.pl_side, self)
            self.kings_dict[BLACK] = self.pl_king
            self.pl_figures.append(self.pl_king)
            self.pl_figures.append(Queen(7, 4, self.pl_side, self))

        if self.pl_side == WHITE:
            self.pl_king = King(7, 4, self.pl_side, self)
            self.kings_dict[WHITE] = self.pl_king
            self.pl_figures.append(self.pl_king)
            self.pl_figures.append(Queen(7, 3, self.pl_side, self))

        self.pl_figures.append(Rook(7, 0, self.pl_side, self))
        self.pl_figures.append(Rook(7, 7, self.pl_side, self))
        self.pl_figures.append(Knight(7, 1, self.pl_side, self))
        self.pl_figures.append(Knight(7, 6, self.pl_side, self))
        self.pl_figures.append(Bishop(7, 2, self.pl_side, self))
        self.pl_figures.append(Bishop(7, 5, self.pl_side, self))

        for i in range(0, 8):
            self.pl_figures.append(Pawn(6, i, self.pl_side, self))

        # Создаем список сделанных во время игры ходов
        self.move_list = []

        # Веса фигур
        self.values_figure = {
            Pawn: 100,
            Knight: 300,
            Bishop: 300,
            Rook: 500,
            Queen: 900,
            King: 9000
        }

        # Веса позиций
        self.values_pos_pl_king = [
            [25, 25, 21, 15, 15, 21, 25, 25],
            [21, 21, 17, 13, 13, 17, 21, 21],
            [13, 13,  5,  5,  5,  5, 13, 13],
            [ 9,  5,  0,  0,  0,  0,  5,  9],
            [ 9,  5,  0,  0,  0,  0,  5,  9],
            [13, 13,  5,  5,  5,  5, 13, 13],
            [21, 21, 17, 13, 13, 17, 21, 21],
            [25, 25, 21, 15, 15, 21, 25, 25]
        ]

        self.values_pos_pl_queen = [
            [20, 25, 25, 30, 30, 25, 25, 20],
            [17, 20, 25, 27, 27, 25, 20, 17],
            [15, 18, 20, 25, 25, 20, 18, 15],
            [12, 15, 19, 21, 21, 19, 15, 12],
            [11, 15, 19, 21, 21, 19, 15, 11],
            [10, 15, 17, 19, 19, 17, 15, 10],
            [ 8, 12, 15, 15, 15, 15, 12,  8],
            [ 7, 10, 15, 20, 20, 15, 10,  7],
        ]

        self.values_pos_pl_rook = [
            [20, 25, 25, 30, 30, 25, 25, 20],
            [17, 20, 25, 27, 27, 25, 20, 17],
            [15, 18, 20, 25, 25, 20, 18, 15],
            [12, 15, 19, 21, 21, 19, 15, 12],
            [11, 15, 19, 21, 21, 19, 15, 11],
            [10, 15, 17, 19, 19, 17, 15, 10],
            [ 8, 12, 15, 15, 15, 15, 12,  8],
            [ 7, 10, 15, 20, 20, 15, 10,  7],
        ]

        self.values_pos_pl_bishop = [
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 22, 18, 18, 18, 18, 22, 14],
            [14, 18, 22, 22, 22, 22, 18, 14],
            [14, 18, 22, 25, 25, 22, 18, 14],
            [14, 18, 22, 25, 25, 22, 18, 14],
            [14, 18, 22, 22, 22, 22, 18, 14],
            [14, 22, 18, 18, 18, 18, 22, 14],
            [14, 14, 14, 14, 14, 14, 14, 14]
        ]

        self.values_pos_pl_knight = [
            [ 0,  4,  8, 10, 10,  8,  4,  0]
            [ 4,  8, 16, 20, 20, 16,  8,  4],
            [ 8, 16, 24, 28, 28, 24, 16,  8],
            [10, 20, 28, 32, 32, 28, 20, 10],
            [10, 20, 28, 32, 32, 28, 20, 10],
            [ 8, 16, 24, 28, 28, 24, 16,  8],
            [ 4,  8, 16, 20, 20, 16,  8,  4],
            [ 0,  4,  8, 10, 10,  8,  4,  0]
        ]

        self.values_pos_pl_pawn = [
            [20, 20, 28, 35, 35, 28, 20, 20],
            [12, 16, 24, 32, 32, 24, 16, 12],
            [12, 16, 24, 32, 32, 24, 16, 12],
            [ 8, 12, 16, 24, 24, 16, 12,  8],
            [ 6,  8, 12, 16, 16, 12,  8,  6],
            [ 6,  8,  8, 12, 12,  8,  8,  6],
            [ 4,  4,  4,  6,  6,  4,  4,  4],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
        ]



    # Метод возвращает оценку позиции на доске с точки зрения компьютера
    def position_evaluation(self):
        # Получаем стоимость фигур компьютера
        cmp_eval = 0
        for figure in self.cmp_figures:
            if figure.is_drop:
                continue
            cmp_eval += self.values_figure[type(figure)]

        # получаем стоимость фигур игрока
        pl_eval = 0
        for figure in self.pl_figures:
            if figure.is_drop:
                continue
            pl_eval += self.values_figure[type(figure)]

        # Возвращаем оценку позиции
        return cmp_eval - pl_eval

    # Метод возвращает количество сделанных ходов
    def get_moves_count(self):
        return len(self.move_list)

    # Метод возвращает все доступные ходы для выбранных фигур (белых или черных)
    def get_all_avl_moves(self, side):
        # Определяем набор фигур, для которого будем получать доступные ходы
        work_list = self.figures_dict[side]

        # Перебираем фигуры из набора
        result = []
        for figure in work_list:
            if figure.is_drop:
                continue
            avl_moves = self.get_avl_moves_for_figure(figure)
            result += avl_moves

        # Возвращаем результат
        return result

    # Метод возвращает список доступных для данной фигуры ходов
    def get_avl_moves_for_figure(self, figure):
        # Список ходов, который будем формировать
        moves = []

        figure_type = type(figure)

        # У пешек есть ряд отличительных особенностей, которые необходимо учитывать при получении доступных ходов:
        # - только пешки бьют и ходят на разные поля
        # - только у пешек есть взятие на проходе
        # - только пешка может превратиться в другую фигуру при достижении края поля (в том числе при взятии)
        # Поэтому код создания ходов для пешек отличается от кода создания ходов для других фигур
        if figure_type == Pawn:
            # Создаем обычные ходы и ход-конверсию при обычном ходе
            actions = figure.get_actions(PAWN_MOVES)
            for new_row, new_col in actions:
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_normal_move(figure, new_row, new_col))

            # Создаем взятия и ход-конверсию при взятии
            actions = figure.get_actions(PAWN_TAKES)
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    continue
                if drop_figure.side == figure.side:
                    continue
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_take_move(figure, new_row, new_col))

            # Создаем ход взятия на проходе
            if self.get_moves_count() > 0:
                last_move = self.move_list[-1]
                if type(last_move.figure) == Pawn and last_move.figure.side != figure.side:
                    r0 = min(last_move.new_row, last_move.old_row)
                    r2 = max(last_move.new_row, last_move.old_row)
                    if (r2 - r0) == 2:
                        c = last_move.new_col
                        for r1, c1 in actions:
                            if r0 < r1 < r2 and c1 == c:
                                moves.append(self.create_passed_take_move(figure, r1, c1, last_move.figure))

        # Проверяем возможность рокировки
        if figure_type == King:
            # Для выполнения рокировки должно быть выполнено множество условий
            # Первое условие - король не должен до рокировки совершать ход
            if not self.was_move(figure):
                # Второе условие - король не должен находится под шахом (то есть поле короля не должно быть "битым")
                if not self.is_strike_cell(figure.row, figure.col, OPPOSITE_SIDE[figure.side]):

                    # Проверяем возможность рокировки с ладьёй слева
                    l_rook = self.get_figure(figure.row, 0)
                    if type(l_rook) == Rook:
                        # Третье условие - ладья не должна ходить
                        if not self.was_move(l_rook):
                            # Получаем список клеток между ладьёй и королём
                            cell_list = [(figure.row, 1), (figure.row, 2)]
                            if figure.col == 4:
                                cell_list.append((figure.row, 3))
                            # Четвертое и пятое условия:
                            # - на клетках между ладьёи королем не должно быть фигур
                            # - эти клетки не должны находиться по ударом
                            # Предполагаем, что эти условия соблюдены и выставляем соответствующее значение flag
                            allowed_cells_flag = True
                            for row_cell, col_cell in cell_list:
                                figure_on_cell = self.get_figure(row_cell, col_cell)
                                if figure_on_cell is not None or self.is_strike_cell(row_cell, col_cell,
                                                                                     OPPOSITE_SIDE[figure.side]):
                                    allowed_cells_flag = False
                                    break
                            # Если все необходимые условия соблюдены, создаем рокировку
                            if allowed_cells_flag:
                                moves.append(
                                    self.create_castling_move(figure, figure.row, figure.col - 2, l_rook, figure.row,
                                                              figure.col - 1))

                    # Проверяем возможность рокировки с ладьёй справа
                    r_rook = self.get_figure(figure.row, 7)
                    if type(r_rook) == Rook:
                        # Третье условие - ладья не должна ходить
                        if not self.was_move(r_rook):
                            # Получаем список клеток между ладьёй и королём
                            cell_list = [(figure.row, 6), (figure.row, 5)]
                            if figure.col == 3:
                                cell_list.append((figure.row, 4))
                            # Четвертое и пятое условия:
                            # - на клетках между ладьёи королем не должно быть фигур
                            # - эти клетки не должны находиться по ударом
                            # Предполагаем, что эти условия соблюдены и выставляем соответствующее значение flag
                            allowed_cells_flag = True
                            for row_cell, col_cell in cell_list:
                                figure_on_cell = self.get_figure(row_cell, col_cell)
                                if figure_on_cell is not None or self.is_strike_cell(row_cell, col_cell,
                                                                                     OPPOSITE_SIDE[figure.side]):
                                    allowed_cells_flag = False
                                    break
                            # Если все необходимые условия соблюдены, создаем рокировку
                            if allowed_cells_flag:
                                moves.append(
                                    self.create_castling_move(figure, figure.row, figure.col + 2, r_rook, figure.row,
                                                              figure.col + 1))

        # Получаем ходы других фигур и короля (за исключением рокировки, являющейся особым ходом)
        if figure_type != Pawn:
            actions = figure.get_actions()
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    moves.append(self.create_normal_move(figure, new_row, new_col))
                    continue
                if drop_figure.side != figure.side:
                    moves.append(self.create_take_move(figure, new_row, new_col))

        # Здесь необходимо вставить код отсечения ходов, ведущих к шаху
        avl_moves = []
        king = self.kings_dict[figure.side]
        for move in moves:
            # Для хода-конверсии создаем фиктивного ферзя
            if move.m_type == CONVERSION:
                move.new_figure = Queen(move.new_row, move.new_col, figure.side, self)

            # Применяем ход
            self.apply_move(move)

            # Проверяем, не находится ли король под ударом
            if not self.is_strike_figure(king):
                avl_moves.append(move)

            # Откатываем ход
            self.cancel_move()

            # Для хода-конверсии удаляем фиктивного ферзя
            if move.m_type == CONVERSION:
                move.new_figure = None

        moves = avl_moves

        # Возвращаем результат
        return moves

    # Метод создает обычный ход
    @staticmethod
    def create_normal_move(figure, new_row, new_col):
        move = Move(NORMAL_MOVE, figure, new_row, new_col)
        return move

    # Метод создает ход-взятие
    def create_take_move(self, figure, new_row, new_col):
        move = Move(TAKE_MOVE, figure, new_row, new_col)
        move.drop_figure = self.get_figure(new_row, new_col)
        return move

    # Метод создает ход-конверсию
    def create_conversion_move(self, figure, new_row, new_col):
        move = Move(CONVERSION, figure, new_row, new_col)
        move.drop_figure = self.get_figure(new_row, new_col)
        move.new_figure = None
        return move

    # Метод создает код взятия на проходе
    @staticmethod
    def create_passed_take_move(figure, new_row, new_col, drop_figure):
        move = Move(PASSED_TAKE, figure, new_row, new_col)
        move.drop_figure = drop_figure
        return move

    # Метод создает ход-рокировку
    @staticmethod
    def create_castling_move(figure, new_row_figure, new_col_figure, rook, new_row_rook, new_col_rook):
        move = Move(CASTLING, figure, new_row_figure, new_col_figure)

        # Фиксируем старое и новое положение ладьи
        move.rook = rook
        move.old_row_rook = rook.row
        move.old_col_rook = rook.col
        move.new_row_rook = new_row_rook
        move.new_col_rook = new_col_rook

        # Возвращаем созданнй ход
        return move

    # Метод применяет переданный ход и вносит его в список совершенных ходов
    def apply_move(self, move):
        # Вносим применяемый ход в список ходов
        self.move_list.append(move)

        # Выполняем действия хода в зависимости от его типа
        # Обычный ход
        if move.m_type == NORMAL_MOVE:
            move.figure.set_pos(move.new_row, move.new_col)
            return

        # Ход-взятие или код-взятие на проходе (алгоритм их выполнения одинаков)
        if move.m_type == TAKE_MOVE or move.m_type == PASSED_TAKE:
            move.figure.set_pos(move.new_row, move.new_col)
            move.drop_figure.is_drop = True
            return

        # Ход-конверсия
        if move.m_type == CONVERSION:
            move.figure.set_pos(move.new_row, move.new_col)
            move.figure.is_drop = True
            if move.drop_figure is not None:
                move.drop_figure.is_drop = True
            self.figures_dict[move.new_figure.side].append(move.new_figure)

        # Рокировка
        if move.m_type == CASTLING:
            move.figure.set_pos(move.new_row, move.new_col)
            move.rook.set_pos(move.new_row_rook, move.new_col_rook)
            return

            # Метод откатывает последний ход из списка совершенных ходов

    # Метод производит откат последнего хода из списка ходов
    def cancel_move(self):
        if self.get_moves_count() == 0:
            return

        # Получаем последний ход
        last_move = self.move_list.pop(-1)

        # Если откатываем обычный ход
        if last_move.m_type == NORMAL_MOVE:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            return

        # Если откатываем ход-взятие или ход-взятие на проходе
        if last_move.m_type == TAKE_MOVE or last_move.m_type == PASSED_TAKE:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.drop_figure.is_drop = False
            return

        # Если откатываем ход-конверсию
        if last_move.m_type == CONVERSION:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.figure.is_drop = False
            if last_move.drop_figure is not None:
                last_move.drop_figure.is_drop = False
            work_list = self.figures_dict[last_move.new_figure.side]
            work_list.remove(last_move.new_figure)
            return

        # Если откатываем рокировку
        if last_move.m_type == CASTLING:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.rook.set_pos(last_move.old_row_rook, last_move.old_col_rook)
            return

    # Метод возвращает True, если поле (row, col) находится под ударом фигур стороны side
    def is_strike_cell(self, row, col, side):
        work_list = self.figures_dict[side]
        for figure in work_list:
            if figure.is_drop:
                continue
            figure_type = type(figure)
            if figure_type == Pawn:
                actions = figure.get_actions(PAWN_TAKES)
            else:
                actions = figure.get_actions()
            for r, c in actions:
                if r == row and c == col:
                    return True

        return False

    # Метод возвращает True, если фигрура находится под ударом фигур противоположной стороны
    def is_strike_figure(self, figure):
        return self.is_strike_cell(figure.row, figure.col, OPPOSITE_SIDE[figure.side])

    # Метод возвращает True, если фигура уже ходила
    def was_move(self, figure):
        for move in self.move_list:
            if figure == move.figure:
                return True
        return False

    # Метод возвращает фигуру, стоящую на клетке r, c
    def get_figure(self, r, c):
        for figure in (self.pl_figures + self.cmp_figures):
            if figure.row == r and figure.col == c and not figure.is_drop:
                return figure
        return None


class SelectorBoard:

    def __init__(self, side, main_board):
        self.queen = Queen(3, 3, side, main_board)
        self.rook = Rook(3, 4, side, main_board)
        self.bishop = Bishop(4, 3, side, main_board)
        self.knight = Knight(4, 4, side, main_board)

    def get_figure(self, r, c):
        if r == 3 and c == 3:
            return self.queen
        if r == 3 and c == 4:
            return self.rook
        if r == 4 and c == 3:
            return self.bishop
        if r == 4 and c == 4:
            return self.knight
