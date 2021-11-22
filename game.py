BLACK = -1
NONE = 0
WHITE = 1


class Cell(object):
    """ Represents the state of a cell in the grid """

    color = NONE

    def __init__(self, color):
        self.color = color

    # Sets the color
    # Returns True if a piece was placed
    # Returns False if a piece could not be placed
    def place_piece(self, color):
        if self.color == NONE:
            self.color = color
            return True
        else:
            return False

    def flip_piece(self, color):
        if self.color != NONE and self.color != color:
            self.color *= -1


class Grid(object):
    """ Represents the grid of Cells """

    def __init__(self, size):
        self.size = size
        self.cells = [[Cell(NONE) for _ in range(size)] for _ in range(size)]

    # Returns True if a piece was placed
    # Returns False if a piece could not be placed
    def place_piece(self, color, position):
        (x, y) = position
        if x >= self.size or y >= self.size:
            # Invalid position
            return False
        result = self.cells[x][y].place_piece(color)

        if result:
            # Piece successfully placed
            # TODO: fix tile logic
            # Let's start with something simpler:
            # Adjacent pieces get turned your color
            adj_tiles = [[0, 1], [1, 1], [1, 0], [1, -1],
                         [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            for x_diff, y_diff in adj_tiles:
                new_x = x + x_diff
                new_y = y + y_diff
                if new_x < self.size and new_y < self.size and new_x >= 0 and new_y >= 0:
                    self.cells[new_x][new_y].flip_piece(color)
            return True
        else:
            # Piece was not placed
            return False

    def matches(self, target):
        board = [[x.color for x in y] for y in self.cells]
        return board == target

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

    def __init__(self, target):
        self.target = target
        self.grid = Grid(len(target))

    # User makes a move
    # position: (x, y) position on the grid
    def move(self, position):
        if self.gameover:
            return
        result = self.grid.place_piece(self.turn, position)
        if result:
            self.num_moves += 1
            self.turn *= -1
            # Check if game is over
            if self.grid.matches(self.target):
                self.gameover = True

    def prettyprint(self):
        print(self.num_moves)
        self.grid.prettyprint()
        print()


if __name__ == "__main__":
    target = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    game = Game(target)
    print("Empty board")
    game.prettyprint()

    game.move((1, 1))
    print("Piece placed at (1, 1)")
    game.prettyprint()

    print("Is the game over?")
    print(game.gameover)
