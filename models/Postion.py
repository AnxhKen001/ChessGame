from typing import Union


class Position:
    def __init__(self, y_pos: Union[str, int], x_pos: Union[str, int], figure):
        self.y = str(y_pos)
        self.x = str(x_pos)
        self.occupied = figure is not None
        self.chess_figure = figure

    def set_chess_figure(self, new_figure):
        self.chess_figure = new_figure
        self.occupy(new_figure is not None)

    def get_chess_figure(self):
        return self.chess_figure

    def occupy(self, new_state):
        self.occupied = new_state

    def to_string(self):
        return str(self.y) + str(self.x)
