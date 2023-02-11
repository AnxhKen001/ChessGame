import json
from models import Postion

figures = {0: 'Pawn', 1: 'Rook', 2: 'Knight', 3: 'Queen', 4: 'King', 5: 'Bishop'}

class ChessFigure:

    def __init__(self, color, title, position, direction, player):
        self.position = position
        self.killed = False
        self.color = color
        self.title = title
        self.direction = direction
        self.moved = False
        self.player = player

    def move(self, new_position: Postion):
        if not self.moved:
            self.set_moved(True)
        self.position.set_chess_figure(None)
        self.position = new_position
        if new_position.occupied:
            self.beat(new_position.get_chess_figure())
        new_position.set_chess_figure(self)

    def set_moved(self, is_moved):
        self.moved = is_moved

    def get_direction(self, direction):
        if direction == "RIGHT" or direction == "TOP":
            return 1
        if direction == "LEFT" or direction == "BOTTOM":
            return -1

    def get_moved(self):
        return self.moved

    def beat(self, figure_to_beat):
        figure_to_beat.eleminate()

    def set_title(self, new_title: str):
        self.title = new_title

    def get_position(self):
        return self.position.to_string()

    def eleminate(self):
        self.killed = True

    def is_position_valid(self, pos: Postion):
        if pos.occupied:
            return pos.chess_figure.color != self.color
        return True

    def get_next_move(self, moving_options):
        if len(moving_options) > 0:
            print("Select the other move: \n")
            for i in range(len(moving_options)):
                print(str(i) + " : " + moving_options[i].to_string())
            new_pos = moving_options[int(input())]
            self.move(new_pos)
            return
        print("None available moves with this figure, choose another one")
        print(json.dumps(figures)[1:-1])
        key = input()
        figure_to_be_moved = figures[int(key)]
        self.player.choose_moving_figure(figure_to_be_moved)
