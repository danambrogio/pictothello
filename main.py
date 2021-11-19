import os
import pygame
from pygame.display import get_surface

MAX_X = 1280
MAX_Y = 720
WINDOW = (MAX_X, MAX_Y)

SCENE_MENU = 0
SCENE_GAME = 1
SCENE_END = 2

EASY = 0
MEDIUM = 1
HARD = 2

TITLE_LOCATION = (450, 100)
EASY_LOCATION = (390, 250)
MEDIUM_LOCATION = (390, 400)
HARD_LOCATION = (390, 550)


def menu(screen):
    running = True

    # UI
    # Background
    bg_image = pygame.image.load(os.path.join("img/background.png")).convert()
    screen.fill((255, 255, 255))
    screen.blit(bg_image, (0, 0))

    # Title
    font = pygame.font.SysFont('Arial', 75)
    title = font.render("PictOthello", True, (30, 30, 30))
    screen.blit(title, TITLE_LOCATION)

    # Menu Buttons
    easy_btn = pygame.image.load(os.path.join(
        "img", "easy_menu_btn.png")).convert()
    med_btn = pygame.image.load(os.path.join(
        "img", "medium_menu_btn.png")).convert()
    hard_btn = pygame.image.load(os.path.join(
        "img", "hard_menu_btn.png")).convert()
    easy = screen.blit(easy_btn, EASY_LOCATION)
    medium = screen.blit(med_btn, MEDIUM_LOCATION)
    hard = screen.blit(hard_btn, HARD_LOCATION)

    while running:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.collidepoint((event.pos)):
                    return SCENE_GAME, EASY
                elif medium.collidepoint((event.pos)):
                    return SCENE_GAME, MEDIUM
                elif hard.collidepoint((event.pos)):
                    return SCENE_GAME, HARD

        pygame.display.flip()
    return (SCENE_END,)


def game(screen, difficulty):
    running = True

    # Set up game screen
    if difficulty == EASY:
        screen.fill((0, 255, 0))
    elif difficulty == MEDIUM:
        screen.fill((0, 0, 255))
    elif difficulty == HARD:
        screen.fill((255, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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


main()
