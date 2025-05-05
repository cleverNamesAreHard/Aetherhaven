import pygame
from ui.main_menu import main_menu
from ui.display_game import display_game
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_ICON_PATH


def main():
    pygame.init()

    # Set video mode first
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Aetherhaven")

    # Now it's safe to load and set the icon
    icon_surface = pygame.image.load(GAME_ICON_PATH)
    pygame.display.set_icon(icon_surface)

    clock = pygame.time.Clock()

    # Show main menu and get game mode (new/load/quit)
    game_mode = main_menu(screen, clock)

    if game_mode == "quit":
        pygame.quit()
        return

    if game_mode == "start_game":
        display_game(screen, clock)

    # Future: handle resume_game, load_game, etc.
    print(f"Selected game mode: {game_mode}")

    pygame.quit()
