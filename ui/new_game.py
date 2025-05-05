# ui/new_game.py
import pygame

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

    running = True
    while running:
        screen.fill((40, 40, 40))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        screen.blit(background, background.get_rect(center=screen.get_rect().center))

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
                    return menu_items[hover_index].lower().replace(" ", "_")

        clock.tick(60)
