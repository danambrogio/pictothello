import os
import pygame
import game as othello

MAX_X = 1280
MAX_Y = 720
WINDOW = (MAX_X, MAX_Y)

SCENE_MENU = 0
SCENE_GAME = 1
SCENE_END = 2

TITLE_LOCATION = (450, 100)
EASY_LOCATION = (390, 250)
MEDIUM_LOCATION = (390, 400)
HARD_LOCATION = (390, 550)

EASY = 5
MEDIUM = 6
HARD = 7

# Just click the squares in order from top left -> right
EZ_TARGET = [[othello.WHITE, othello.BLACK, othello.WHITE, othello.WHITE], [othello.WHITE, othello.BLACK, othello.WHITE, othello.WHITE], [
    othello.WHITE, othello.BLACK, othello.WHITE, othello.WHITE], [othello.WHITE, othello.BLACK, othello.WHITE, othello.WHITE]]
MD_TARGET = [[], [], [], [], [], []]
HD_TARGET = [[], [], [], [], [], [], []]

BOARD_LOCATION = (200, 300)
TARGET_LOCATION = (900, 300)
BOARD_COLOR = (125, 109, 59)
LINE_COLOR = (40, 40, 40)
LINE_WIDTH = 15
EASY_TILE_LOCATIONS = [[(16, 16), (81, 16), (146, 16), (211, 16)], [(16, 81), (81, 81), (146, 81), (211, 81)], [
    (16, 146), (81, 146), (146, 146), (211, 146)], [(16, 211), (81, 211), (146, 211), (211, 211)]]


def menu(screen):
    running = True

    # Load images
    bg_img = pygame.image.load(os.path.join("img", "menu_bg.png")).convert()
    easy_img = pygame.image.load(os.path.join(
        "img", "easy_menu_btn.png")).convert()
    med_img = pygame.image.load(os.path.join(
        "img", "medium_menu_btn.png")).convert()
    hard_img = pygame.image.load(os.path.join(
        "img", "hard_menu_btn.png")).convert()

    # UI
    # Background
    screen.fill((255, 255, 255))
    screen.blit(bg_img, (0, 0))

    # Title
    title_font = pygame.font.SysFont('Arial', 75)
    title = title_font.render("PictOthello", True, (30, 30, 30))
    screen.blit(title, TITLE_LOCATION)

    # Menu Buttons
    easy_btn = screen.blit(easy_img, EASY_LOCATION)
    medium_btn = screen.blit(med_img, MEDIUM_LOCATION)
    hard_btn = screen.blit(hard_img, HARD_LOCATION)

    while running:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint((event.pos)):
                    return SCENE_GAME, EASY
                elif medium_btn.collidepoint((event.pos)):
                    return SCENE_GAME, MEDIUM
                elif hard_btn.collidepoint((event.pos)):
                    return SCENE_GAME, HARD

        pygame.display.flip()
    return (SCENE_END,)


def game(screen, difficulty):
    running = True

    # Load images
    bg_img = pygame.image.load(os.path.join(
        "img", "game_bg.png")).convert_alpha()
    bg_img = pygame.transform.smoothscale(bg_img, WINDOW)

    black = pygame.image.load(os.path.join("img", "black.png")).convert_alpha()
    black = pygame.transform.smoothscale(black, (50, 50))
    white = pygame.image.load(os.path.join("img", "white.png")).convert_alpha()
    white = pygame.transform.smoothscale(white, (50, 50))

    # Set up game screen
    if difficulty == EASY:
        game = othello.Game(EZ_TARGET)
        screen.fill((0, 250, 0))
        screen.blit(bg_img, (0, 0))
        # Create board surface
        board = draw_easy_board()
        target = draw_easy_board()
        # fill in target based on game.target
        fill_in_target(target, game.target, (black, white))
        screen.blit(board, BOARD_LOCATION)
        screen.blit(target, TARGET_LOCATION)
        # get a list of rects for each square on the board
        rects = [[pygame.Rect(x_point, y_point, 50, 50) for (
            x_point, y_point) in row] for row in EASY_TILE_LOCATIONS]

    elif difficulty == MEDIUM:
        game = othello.Game(MD_TARGET)
        screen.fill((0, 0, 250))
        screen.blit(bg_img, (0, 0))
    elif difficulty == HARD:
        game = othello.Game(HD_TARGET)
        screen.fill((250, 0, 0))
        screen.blit(bg_img, (0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (board_x, board_y) = BOARD_LOCATION
                (click_x, click_y) = event.pos
                click_x -= board_x
                click_y -= board_y

                # check in x/y falls within one of the tiles
                for y in range(len(rects)):
                    for x in range(len(rects[y])):
                        if rects[x][y].collidepoint((click_x, click_y)):
                            game.move((x, y))
                            fill_in_board(board, game.grid.cells,
                                          (black, white))
                            screen.blit(board, BOARD_LOCATION)
        pygame.display.flip()
        if game.gameover:
            # Victory
            screen.fill((0, 255, 0))

    return SCENE_MENU


def draw_easy_board():
    board = pygame.Surface((275, 275))
    board.fill(BOARD_COLOR)
    # outside lines
    pygame.draw.line(board, LINE_COLOR, (0, 0), (0, 275), (LINE_WIDTH * 2))
    pygame.draw.line(board, LINE_COLOR, (0, 0), (275, 0), (LINE_WIDTH * 2))
    pygame.draw.line(board, LINE_COLOR, (275, 275), (0, 275), (LINE_WIDTH * 2))
    pygame.draw.line(board, LINE_COLOR, (275, 275), (275, 0), (LINE_WIDTH * 2))
    # inside lines
    for x in (73, 138, 203):
        pygame.draw.line(board, LINE_COLOR, (x, 0), (x, 275), LINE_WIDTH)
    for y in (73, 138, 203):
        pygame.draw.line(board, LINE_COLOR, (0, y), (275, y), LINE_WIDTH)

    return board


def fill_in_board(board, grid, tiles):
    (black, white) = tiles
    # go through grid's [][] and place tokens based on values
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[x][y].color == othello.BLACK:
                board.blit(black, EASY_TILE_LOCATIONS[x][y])
            elif grid[x][y].color == othello.WHITE:
                board.blit(white, EASY_TILE_LOCATIONS[x][y])


def fill_in_target(board, grid, tiles):
    (black, white) = tiles
    # go through grid's [][] and place tokens based on values
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[x][y] == othello.BLACK:
                board.blit(black, EASY_TILE_LOCATIONS[x][y])
            elif grid[x][y] == othello.WHITE:
                board.blit(white, EASY_TILE_LOCATIONS[x][y])


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    scene = SCENE_MENU
    difficulty = EASY
    running = True
    while running:
        if scene == SCENE_MENU:
            scene, *difficulty = menu(screen)
        elif scene == SCENE_GAME:
            scene = game(screen, *difficulty)
        elif scene == SCENE_END:
            running = False
    pygame.quit()


if __name__ == "__main__":
    main()
    pygame.quit()
