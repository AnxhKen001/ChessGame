from enum import Enum

from models import Postion
from models.ChessBoard import ChessBoard
from models.ChessFigure import ChessFigure

figures = {0: 'Pawn', 1: 'Rook', 2: 'Knight', 3: 'Queen', 4: 'King', 5: 'Bishop'}


class Board(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Directions(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP = 'TOP'
    BOTTOM = "BOTTOM"


extremes = {
    Directions.LEFT: 0,
    Directions.RIGHT: 7,
    Directions.BOTTOM: 0,
    Directions.TOP: 7,
}


class CrossDirections(Enum):
    LEFT_TOP = 'LEFT_TOP'
    RIGHT_TOP = 'RIGHT_TOP'
    LEFT_BOTTOM = 'LEFT_BOTTOM'
    RIGHT_BOTTOM = "RIGHT_BOTTOM"


def get_horizontal_moves(figure, x, y,
                         direction):
    index_of_coordinate_to_be_moved = get_x_index(x)

    def get_condition():
        condition = index_of_coordinate_to_be_moved >= extremes[direction]

        if direction == Directions.RIGHT:
            condition = index_of_coordinate_to_be_moved <= extremes[direction]
        return condition

    moves_arr = []
    while get_condition():
        pos = get_position(ChessBoard.x_positions[index_of_coordinate_to_be_moved], y)
        if figure.is_position_valid(pos):
            moves_arr.append(pos)
            index_of_coordinate_to_be_moved = index_of_coordinate_to_be_moved + figure.get_direction(direction) * 1
            if pos.occupied:
                break
            continue

        index_of_coordinate_to_be_moved = index_of_coordinate_to_be_moved + figure.get_direction(direction) * 1
        break_condition = pos.to_string() != figure.position.to_string()
        if break_condition:
            break
    return moves_arr


def get_vertical_moves(figure, x, y, direction):
    figure.direction = direction

    index_of_coordinate_to_be_moved = get_y_index(y)

    def get_condition():
        condition = index_of_coordinate_to_be_moved >= extremes[direction]

        if direction == Directions.TOP:
            condition = index_of_coordinate_to_be_moved <= extremes[direction]
        return condition

    moves_arr = []
    while get_condition():
        pos = get_position(x, ChessBoard.y_positions[index_of_coordinate_to_be_moved])
        if figure.is_position_valid(pos):
            moves_arr.append(pos)
            index_of_coordinate_to_be_moved = index_of_coordinate_to_be_moved + figure.get_direction(direction) * 1
            continue
        index_of_coordinate_to_be_moved = index_of_coordinate_to_be_moved + figure.get_direction(direction) * 1
        break_condition = pos.to_string() != figure.position.to_string()
        if break_condition:
            break
    return moves_arr


def get_diagonal_moves(figure, position, cross_direction):
    x = position.x
    y = position.y
    initial_x_index = get_x_index(x)
    initial_y_index = get_y_index(y)

    def get_condition(x_index, y_index):
        condition = x_index <= extremes[Directions.RIGHT] and y_index <= extremes[Directions.TOP]
        if cross_direction == CrossDirections.LEFT_BOTTOM:
            condition = x_index >= extremes[Directions.LEFT] and y_index >= extremes[Directions.BOTTOM]
        return condition

    direction = 1 if cross_direction == CrossDirections.RIGHT_TOP else -1

    return get_diagonal_moves_by_dir(figure, direction, direction, initial_x_index, initial_y_index, get_condition)


def get_diagonal_moves_by_dir(figure, x_direction, y_direction, x_index, y_index, get_condition):
    moves_arr = []

    while get_condition(x_index, y_index):
        pos = get_position(ChessBoard.x_positions[x_index], ChessBoard.y_positions[y_index])
        if figure.is_position_valid(pos):
            moves_arr.append(pos)
            x_index = x_index + x_direction * 1
            y_index = y_index + y_direction * 1
            if pos.occupied:
                break
            continue
        x_index = x_index + x_direction * 1
        y_index = y_index + y_direction * 1
        break_condition = pos.to_string() != figure.position.to_string()
        if break_condition:
            break

    return moves_arr


def get_position(x, y):
    try:
        y_index = ChessBoard.y_positions.index(int(y))
        x_index = ChessBoard.x_positions.index(x)
    except IndexError:
        return None
    return ChessBoard.positions[y_index][x_index]


def get_figures_by_name(name):
    matching_figures = []
    for y in range(len(ChessBoard.y_positions)):
        for x in range(len(ChessBoard.x_positions)):
            if type(ChessBoard.positions[y][x].chess_figure).__name__ == name:
                matching_figures.append(ChessBoard.positions[y][x].chess_figure)
    return matching_figures


def get_x_index(x: str):
    return ChessBoard.x_positions.index(x)


def get_y_index(y):
    return ChessBoard.y_positions.index(int(y))


def get_x(x_index: int):
    try:
        return ChessBoard.x_positions[x_index]
    except IndexError:
        return None


def get_digonal_moves_2(figure, position, cross_direction):
    x = position.x
    y = position.y
    initial_x_index = get_x_index(x)
    initial_y_index = get_y_index(y)

    y_direction = 1 if cross_direction == CrossDirections.LEFT_TOP else -1
    x_direction = 1 if cross_direction == CrossDirections.RIGHT_BOTTOM else -1

    def get_condition(x_index, y_index):
        condition = x_index >= extremes[Directions.LEFT] and y_index <= extremes[Directions.TOP]
        if cross_direction == CrossDirections.RIGHT_BOTTOM:
            condition = x_index <= extremes[Directions.RIGHT] and y_index >= extremes[Directions.BOTTOM]
        return condition

    return get_diagonal_moves_by_dir(figure, x_direction, y_direction, initial_x_index, initial_y_index, get_condition)


class Pawn(ChessFigure):

    def __init__(self, color: str, title: str, position: Postion, direction, player):
        super().__init__(color, title, position, direction, player)

    def get_moves(self):
        possible_moves = []
        y = int(self.position.y) + self.direction
        pos = get_position(self.position.x, y)
        if not pos.occupied:
            possible_moves.append(pos)
        return possible_moves

    def get_moving_options(self):
        options = self.get_moves()
        self.get_next_move(options)


class Bishop(ChessFigure):
    def __init__(self, color: str, title: str, position: Postion, direction, player):
        super().__init__(color, title, position, direction, player)

    def get_moves(self):
        moves_1 = get_diagonal_moves(self, self.position, CrossDirections.RIGHT_TOP)
        moves_2 = get_diagonal_moves(self, self.position, CrossDirections.LEFT_BOTTOM)
        moves_3 = get_digonal_moves_2(self, self.position, CrossDirections.LEFT_TOP)
        moves_4 = get_digonal_moves_2(self, self.position, CrossDirections.RIGHT_BOTTOM)

        return moves_1 + moves_2 + moves_3 + moves_4

    def get_moving_options(self):
        moving_options = self.get_moves()
        self.get_next_move(moving_options)


class King(ChessFigure):
    def __init__(self, color: str, title: str, position: Postion, direction, player):
        super().__init__(color, title, position, direction, player)
        self.side = Board.RIGHT
        self.castling_done = False
        self.in_check = False
        self.figures_that_threaten_check = []

    def set_board_side(self, new_side):
        self.side = new_side

    def get_figures_that_threaten_check(self):
        return self.figures_that_threaten_check

    def is_position_in_check(self, position_to_test):
        other_player = self.player.get_other_player()
        for figure in other_player.player_figures:
            figure_moves = figure.get_moves()
            figure_causes_check = len(
                list(filter(lambda pos: pos.to_string() == position_to_test.to_string(), figure_moves))) > 0
            if figure_causes_check:
                return True
        return False

    def get_moves(self):
        starting_x_index = get_x_index(self.position.x) - 1
        starting_y_index = get_y_index(self.position.y) - 1
        x_indexes = [starting_x_index, starting_x_index + 1, starting_x_index + 2]
        y_indexes = [starting_y_index, starting_y_index + 1, starting_y_index + 2]
        moves_arr = []

        for y_index in y_indexes:
            if y_index < 0 or y_index > 7:
                continue
            y = ChessBoard.y_positions[y_index]
            for x_index in x_indexes:
                if x_index < 0 or x_index > 7:
                    continue
                x = ChessBoard.x_positions[x_index]
                pos = get_position(x, y)
                if self.is_position_valid(pos):
                    moves_arr.append(pos)

        return moves_arr

    def check_move_for_board_side(self, pos):
        if pos.x < 'E':
            self.set_board_side(Board.LEFT)
        else:
            self.set_board_side(Board.RIGHT)

    def get_castling(self):
        return self.castling_done

    def set_castling(self):
        return self.castling_done

    def get_moving_options(self):
        moves = self.get_moves()
        king_valid_moves = list(filter(lambda pos: not self.is_position_in_check(pos), moves))
        if len(king_valid_moves) > 0:
            print("Select next move: \n")
            for i in range(len(king_valid_moves)):
                print(str(i) + " : " + king_valid_moves[i].to_string())
            new_pos = king_valid_moves[int(input())]
            self.check_move_for_board_side(new_pos)
            self.move(new_pos)
            return
        self.get_next_move(king_valid_moves)


class Knight(ChessFigure):
    def __init__(self, color, title, position, direction, player):
        super().__init__(color, title, position, direction, player)

    def get_knight_moves(self, x_step, y_step):
        x_index = get_x_index(self.position.x)
        y_index = get_y_index(self.position.y)
        new_y_indexes = [y_index + y_step, y_index - y_step]
        new_x_index_1 = x_index + x_step
        new_x_index_2 = x_index - x_step
        moves_arr = []
        for index_y in new_y_indexes:
            if index_y > 7 or index_y < 0:
                continue
            try:
                y = ChessBoard.y_positions[index_y]
            except IndexError:
                continue

            for i_of_x in [new_x_index_1, new_x_index_2]:
                if i_of_x > 7 or i_of_x < 0:
                    continue
                x = 'A'
                x = ChessBoard.x_positions[i_of_x]
                pos = get_position(x, y)
                if self.is_position_valid(pos):
                    moves_arr.append(pos)
        return moves_arr

    def get_moves(self):
        vmoves = self.get_knight_moves(1, 2)
        hmoves = self.get_knight_moves(2, 1)
        return vmoves + hmoves

    def get_moving_options(self):
        moves = self.get_moves()
        self.get_next_move(moves)


class Queen(ChessFigure):
    def __init__(self, color: str, title: str, position: Postion, direction, player):
        super().__init__(color, title, position, direction, player)

    def get_moves(self):
        x = self.position.x
        y = self.position.y
        lpos = get_horizontal_moves(self, x, y, Directions.LEFT)
        rpos = get_horizontal_moves(self, x, y, Directions.RIGHT)
        t_pos = get_vertical_moves(self, x, y, Directions.TOP)
        bpos = get_vertical_moves(self, x, y, Directions.BOTTOM)
        trmoves = get_diagonal_moves(self, self.position, CrossDirections.RIGHT_TOP)
        tlmoves = get_diagonal_moves(self, self.position, CrossDirections.LEFT_BOTTOM)
        tlmoves = get_digonal_moves_2(self, self.position, CrossDirections.LEFT_TOP)
        rbmove = get_digonal_moves_2(self, self.position, CrossDirections.RIGHT_BOTTOM)
        return lpos + rpos + t_pos + bpos + trmoves + tlmoves + tlmoves + rbmove

    def get_moving_options(self):
        moves = self.get_moves()
        self.get_next_move(moves)


class Rook(ChessFigure):
    def __init__(self, color: str, title: str, position: Postion, direction, player):
        super().__init__(color, title, position, direction, player)

    def get_moves(self):
        x = self.position.x
        y = self.position.y
        lpos = get_horizontal_moves(self, x, y, Directions.LEFT)
        rpos = get_horizontal_moves(self, x, y, Directions.RIGHT)
        tpos = get_vertical_moves(self, x, y, Directions.TOP)
        bpos = get_vertical_moves(self, x, y, Directions.BOTTOM)
        return lpos + rpos + tpos + bpos

    def get_moving_options(self):
        moves = self.get_moves()
        self.get_next_move(moves)
