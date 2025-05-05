import pygame
import os
from core.config import FONT_PATH, MENU_LOGO_PATH, MENU_BACKGROUND_PATH
from ui.new_game import new_game_menu

def has_save_files():
    save_dir = "save_data"
    return any(file.endswith(".json") for file in os.listdir(save_dir))

def main_menu(screen, clock):
    font = pygame.font.Font(FONT_PATH, 30)

    # Load assets
    logo = pygame.image.load(MENU_LOGO_PATH).convert_alpha()
    logo_rect = logo.get_rect()

    background = pygame.image.load(MENU_BACKGROUND_PATH).convert_alpha()
    background.set_alpha(int(255 * 0.15))
    bg_rect = background.get_rect(center=screen.get_rect().center)

    # Dynamically build menu
    menu_items = []
    if has_save_files():
        menu_items.append("Resume Game")
    menu_items += ["New Game", "Load Game", "Settings", "Quit"]

    spacing_between_logo_and_menu = 20
    spacing_between_items = 50

    item_surfaces = [font.render(item, True, (255, 255, 255)) for item in menu_items]
    total_menu_height = logo_rect.height + spacing_between_logo_and_menu + len(menu_items) * spacing_between_items
    top_offset = (screen.get_height() - total_menu_height) // 2

    logo_rect.centerx = screen.get_width() // 2
    logo_rect.top = top_offset

    item_rects = [
        surf.get_rect(centerx=screen.get_width() // 2,
                      top=logo_rect.bottom + spacing_between_logo_and_menu + i * spacing_between_items)
        for i, surf in enumerate(item_surfaces)
    ]

    running = True
    while running:
        screen.fill((40, 40, 40))
        screen.blit(background, bg_rect)

        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        screen.blit(logo, logo_rect)

        for i, rect in enumerate(item_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i

        for i, (surf, rect) in enumerate(zip(item_surfaces, item_rects)):
            if i == hover_index:
                hover_box = rect.inflate(20, 10)
                hover_box.center = rect.center
                pygame.draw.rect(screen, (100, 100, 100), hover_box)
            screen.blit(surf, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_index is not None:
                    selection = menu_items[hover_index].lower().replace(" ", "_")

                    if selection == "new_game":
                        result = new_game_menu(screen, clock, font, background)
                        if result == "start_game":
                            return result
                        elif result == "quit":
                            return "quit"
                        elif result == "back":
                            continue  # Stay on menu
                    else:
                        return selection

        clock.tick(60)
