from models.Postion import Position


def fill_board():
    for number in ChessBoard.y_positions:
        positions = [] * len(ChessBoard.x_positions)
        for letter in ChessBoard.x_positions:
            positions.append(Position(number, letter, None))
        ChessBoard.positions.insert(number - 1, positions)


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


def get_x_index(x):
    return ChessBoard.x_positions.index(x)


def get_y_index(y):
    return ChessBoard.y_positions.index(int(y))


def get_x(x_index):
    try:
        return ChessBoard.x_positions[x_index]
    except IndexError:
        return None


class ChessBoard:
    x_positions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    y_positions = [1, 2, 3, 4, 5, 6, 7, 8]
    positions = [] * len(y_positions)

    def __init__(self):
        fill_board()
