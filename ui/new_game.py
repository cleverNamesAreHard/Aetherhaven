import pygame
from core import game_state
from world.world_generation import WorldGenerator

def new_game_menu(screen, clock, font, background):
    menu_items = ["Tutorial", "New Game"]
    spacing_between_items = 50

    item_surfaces = [font.render(item, True, (255, 255, 255)) for item in menu_items]
    total_menu_height = len(menu_items) * spacing_between_items
    top_offset = (screen.get_height() - total_menu_height) // 2

    item_rects = [
        surf.get_rect(centerx=screen.get_width() // 2,
                      top=top_offset + i * spacing_between_items)
        for i, surf in enumerate(item_surfaces)
    ]

    # Back button setup
    back_text = "Back"
    back_surf = font.render(back_text, True, (255, 255, 255))
    back_rect = back_surf.get_rect(topleft=(30, screen.get_height() - 60))

    running = True
    while running:
        screen.fill((40, 40, 40))
        screen.blit(background, background.get_rect(center=screen.get_rect().center))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None
        back_hovered = back_rect.collidepoint(mouse_pos)

        for i, rect in enumerate(item_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i

        for i, (surf, rect) in enumerate(zip(item_surfaces, item_rects)):
            if i == hover_index:
                hover_box = rect.inflate(20, 10)
                hover_box.center = rect.center
                pygame.draw.rect(screen, (100, 100, 100), hover_box)
            screen.blit(surf, rect)

        # Draw back button
        if back_hovered:
            pygame.draw.rect(screen, (100, 100, 100), back_rect.inflate(20, 10))
        screen.blit(back_surf, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_hovered:
                    return "back"
                if hover_index is not None:
                    result = menu_items[hover_index].lower().replace(" ", "_")
                    if result == "new_game":
                        map_size = select_map_size(screen, clock, font, background)
                        if map_size:
                            generator = WorldGenerator(map_size)
                            filepath = generator.generate_and_save()
                            game_state.current_save_path = filepath
                            return "start_game"
                        else:
                            continue  # go back to this screen
                    return result

        clock.tick(60)


def select_map_size(screen, clock, font, background):
    size_options = [("100 x 100", 100), ("200 x 200", 200), ("300 x 300", 300)]
    selected_index = 0
    spacing_between_items = 60

    begin_text = "Begin Game"
    begin_surf = font.render(begin_text, True, (255, 255, 255))
    begin_rect = begin_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))

    option_surfaces = [font.render(label, True, (255, 255, 255)) for label, _ in size_options]
    option_rects = [
        surf.get_rect(centerx=screen.get_width() // 2,
                      top=200 + i * spacing_between_items)
        for i, surf in enumerate(option_surfaces)
    ]

    # Back button setup
    back_text = "Back"
    back_surf = font.render(back_text, True, (255, 255, 255))
    back_rect = back_surf.get_rect(topleft=(30, screen.get_height() - 60))

    running = True
    while running:
        screen.fill((40, 40, 40))
        screen.blit(background, background.get_rect(center=screen.get_rect().center))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None
        begin_hovered = begin_rect.collidepoint(mouse_pos)
        back_hovered = back_rect.collidepoint(mouse_pos)

        for i, rect in enumerate(option_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i

        for i, (surf, rect) in enumerate(zip(option_surfaces, option_rects)):
            if i == selected_index or i == hover_index:
                box = rect.inflate(20, 10)
                box.center = rect.center
                pygame.draw.rect(screen, (100, 100, 100), box)
            screen.blit(surf, rect)

        # Draw Begin Game button
        pygame.draw.rect(screen, (120, 80, 80) if begin_hovered else (80, 80, 80), begin_rect.inflate(30, 20))
        screen.blit(begin_surf, begin_rect)

        # Draw Back button
        if back_hovered:
            pygame.draw.rect(screen, (100, 100, 100), back_rect.inflate(20, 10))
        screen.blit(back_surf, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_hovered:
                    return None  # Go back to new_game_menu
                if begin_hovered:
                    return size_options[selected_index][1]
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_index = i

        clock.tick(60)
