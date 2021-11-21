import os
import pygame
import game as othello

MAX_X = 1280
MAX_Y = 720
WINDOW = (MAX_X, MAX_Y)

SCENE_MENU = 0
SCENE_GAME = 1
SCENE_END = 2

# Difficulty = size of grid
EASY = 5
MEDIUM = 6
HARD = 7

EZ_TARGET = [[1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [
    0, -1, -1, -1, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1]]
MD_TARGET = [[], [], [], [], [], []]
HD_TARGET = [[], [], [], [], [], [], []]

TITLE_LOCATION = (450, 100)
EASY_LOCATION = (390, 250)
MEDIUM_LOCATION = (390, 400)
HARD_LOCATION = (390, 550)


def menu(screen):
    running = True

    # Load images
    bg_img = pygame.image.load(os.path.join("img", "background.png")).convert()
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
    black = pygame.image.load(os.path.join("img", "black.png")).convert_alpha()
    black = pygame.transform.smoothscale(black, (50, 50))

    white = pygame.image.load(os.path.join("img", "white.png")).convert_alpha()
    white = pygame.transform.smoothscale(white, (50, 50))

    # Set up game screen
    if difficulty == EASY:
        game = othello.Game(EZ_TARGET)
        screen.blit(black, (300, 300))
        screen.blit(white, (300, 400))
    elif difficulty == MEDIUM:
        game = othello.Game([])
        screen.fill((0, 0, 255))
    elif difficulty == HARD:
        game = othello.Game([])
        screen.fill((255, 0, 0))

    # Draw game screen
    # See readme for design description

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # test if user clicked on cell
                # pass action to given cell
                # determine if game is over
                pass
        pygame.display.flip()

    return SCENE_MENU


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
