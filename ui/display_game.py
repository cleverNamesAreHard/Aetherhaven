import json
import pygame
from collections import Counter
from core import game_state

BIOME_COLORS = {
    "water": (28, 107, 160),
    "beach": (238, 214, 175),
    "grassland": (106, 190, 48),
    "forest": (34, 139, 34),
    "mountain": (139, 137, 137),
    "desert": (237, 201, 175),
    "farmland": (181, 101, 29),
    "hill": (160, 132, 79)
}

RESOURCE_COLORS = {
    "wood": (0, 100, 0),
    "gold": (255, 215, 0),
    "food": (255, 165, 0),
}


def display_game(screen, clock):
    if not game_state.current_save_path:
        print("No save file loaded.")
        return

    with open(game_state.current_save_path, "r") as f:
        data = json.load(f)

    tiles = data["tiles"]
    width = data["width"]
    height = data["height"]

    biomes = Counter(tile["biome"].lower().strip() for tile in tiles)
    print("Biome distribution:", biomes)
    print("Unique biomes in file:", list(biomes.keys()))

    tile_size = min(screen.get_width() // width, screen.get_height() // height)
    offset_x = (screen.get_width() - (width * tile_size)) // 2
    offset_y = (screen.get_height() - (height * tile_size)) // 2

    print(
        f"Tile size: {tile_size}, screen: {
            screen.get_width()}x{
            screen.get_height()}")

    tile_map = {}
    for tile in tiles:
        x = int(tile["x"])
        y = int(tile["y"])
        tile_map[(x, y)] = tile

    running = True
    while running:
        screen.fill((0, 0, 0))

        for (x, y), tile in tile_map.items():
            biome = tile.get("biome", "unknown").lower().strip()
            color = BIOME_COLORS.get(biome, (255, 0, 0))  # bright red fallback

            rect = pygame.Rect(
                offset_x + x * tile_size,
                offset_y + y * tile_size,
                tile_size,
                tile_size
            )

            pygame.draw.rect(screen, color, rect)

            if tile_size > 4:
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            for resource_type, value in tile.get("resources", {}).items():
                if value > 0 and resource_type in RESOURCE_COLORS:
                    dot_color = RESOURCE_COLORS[resource_type]
                    center = rect.center
                    radius = max(2, tile_size // 6)
                    pygame.draw.circle(screen, dot_color, center, radius)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        clock.tick(60)
