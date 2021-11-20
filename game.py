BLACK = -1
NONE = 0
WHITE = 1


class Cell(object):
    """ Represents the state of a cell in the grid """

    color = NONE

    def __init__(self, color):
        self.color = color

    # Sets the color
    # Returns 1 if a piece was placed
    # Returns 0 if a piece could not be placed
    def place_piece(self, color):
        if self.color == NONE:
            self.color = color
            return 1
        else:
            return 0


class Grid(object):
    """ Represents the grid of Cells """

    def __init__(self, size):
        self.size = size
        self.cells = [[Cell(NONE) for _ in range(size)] for _ in range(size)]

    # Returns 1 if a piece was placed
    # Returns 0 if a piece could not be placed
    def place_piece(self, color, position):
        (x, y) = position
        if x >= self.size or y >= self.size:
            return 0
        return self.cells[y][x].place_piece(color)

        # Update other cells if surrounding
        # Look up, left, right, down, diagonal
        # If piece beside is opposite-color, check if capturing:
        #   If oxo, x becomes o
        #   If oxxxo, xxx becomes ooo

    # Prettyprint for debug purposes only
    def prettyprint(self):
        for y in self.cells:
            for x in y:
                print(x.color, end="")
            print()


class Game(object):
    """ Represents the current state of the game """
    gameover = False
    num_moves = 0
    turn = BLACK

    def __init__(self, difficulty):
        self.grid = Grid(difficulty)

    # User makes a move
    # position: (x, y) position on the grid
    def move(self, position):
        result = self.grid.place_piece(self.turn, position)
        if result == 1:
            self.num_moves += 1
            self.turn *= -1

    def prettyprint(self):
        self.grid.prettyprint()


if __name__ == "__main__":
    game = Game(3)
    print("Empty board")
    game.prettyprint()

    game.move((0, 0))
    print("Piece placed at (0, 0)")
    game.prettyprint()

    game.move((1, 1))
    print("Piece placed at (1, 1)")
    game.prettyprint()

    game.move((1, 1))
    print("Piece failed to be placed at (1, 1)")
    game.prettyprint()

    game.move((2, 2))
    print("Piece placed at (2, 2), capturing")
    game.prettyprint()
