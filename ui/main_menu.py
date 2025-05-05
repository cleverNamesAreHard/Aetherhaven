import pygame
import os

def main_menu(screen, clock):
    font_path = "assets/fonts/Crimson_Pro/CrimsonPro-VariableFont_wght.ttf"
    font = pygame.font.Font(font_path, 28)
    menu_items = ["Resume Game", "New Game", "Load Game", "Settings", "Quit"]

    # Load and position logo
    logo_path = "assets/logos/logo256.png"
    logo = pygame.image.load(logo_path).convert_alpha()
    logo_rect = logo.get_rect()

    # Load background image
    bg_path = "assets/images/main_menu_background.png"
    background = pygame.image.load(bg_path).convert_alpha()
    background.set_alpha(int(255 * 0.15))  # 15% opacity

    # Center the background on the screen
    bg_rect = background.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Layout calculations
    spacing_between_logo_and_menu = 20
    spacing_between_items = 50
    item_surfaces = [font.render(item, True, (255, 255, 255)) for item in menu_items]

    total_menu_height = (
        logo_rect.height +
        spacing_between_logo_and_menu +
        len(menu_items) * spacing_between_items
    )
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
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        # Draw semi-transparent background image
        screen.blit(background, bg_rect)

        # Draw logo
        screen.blit(logo, logo_rect)

        # Check hover
        for i, rect in enumerate(item_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i

        # Draw menu items
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
                    return menu_items[hover_index].lower().replace(" ", "_")

        clock.tick(60)
