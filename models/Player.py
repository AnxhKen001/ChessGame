from models.ChessBoard import ChessBoard
from models.Figures import Rook, Knight, Bishop, Queen, King, Pawn
from models.Postion import Position

initial_figures_mapping = {
    '1A': Rook,
    '8A': Rook,
    '1H': Rook,
    '8H': Rook,
    '1B': Knight,
    '8B': Knight,
    '1G': Knight,
    '8G': Knight,
    '1C': Bishop,
    '8C': Bishop,
    '1F': Bishop,
    '8F': Bishop,
    '1D': Queen,
    '8D': Queen,
    '1E': King,
    '8E': King
}


class Player:
    number_of_figures = 16

    def __init__(self, number, name, color, game):
        self.number = number
        self.name = name
        self.figures_color = color
        self.game = game
        self.player_figures = [] * self.number_of_figures
        self.init_figures()

    def init_figures(self):
        initial_indexes_for_player = []
        if self.number == 0:
            initial_indexes_for_player.extend((0, 1))
        else:
            initial_indexes_for_player.extend([6, 7])

        for index_of_number in range(len(ChessBoard.y_positions)):
            for index_of_letter in range(len(ChessBoard.x_positions)):
                if index_of_number not in initial_indexes_for_player:
                    continue
                pos: Position = ChessBoard.positions[index_of_number][index_of_letter]
                figure = None
                direction = 1
                if self.number == 1:
                    direction = -1
                if index_of_number == 1 or index_of_number == 6:
                    figure = Pawn(self.figures_color, '', pos, direction, self)
                else:
                    figure = initial_figures_mapping[pos.to_string()](
                        self.figures_color, '', pos, direction, self)
                figure.set_title(type(figure).__name__)
                pos.set_chess_figure(figure)
                self.player_figures.append(figure)

    def get_other_player(self):
        return list(filter(lambda p: p.number != self.number, self.game.players))[0]

    def move_figure(self, figure_to_be_moved):
        figure_to_be_moved.get_moving_options()

    def choose_moving_figure(self, figure_to_be_moved: str):
        matching_figures = []
        for figure in self.player_figures:
            if type(figure).__name__ == figure_to_be_moved and not figure.killed:
                matching_figures.append(figure)
        if len(matching_figures) == 0:
            print("Figure dissabled")
        elif len(matching_figures) == 1:
            self.move_figure(matching_figures[0])
        else:
            print("Which " + figure_to_be_moved + " you want to move: \n")
            for index in range(len(matching_figures)):
                print(str(index) + " : " + matching_figures[index].get_position() + "\n")
            self.move_figure(matching_figures[int(input())])
