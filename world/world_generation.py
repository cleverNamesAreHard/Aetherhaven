import numpy as np
import random
import os
import json
from datetime import datetime
from scipy.spatial import Voronoi, KDTree
from noise import snoise2
from world.tile import Tile
import pygame

# === Tunable thresholds and generation weights ===

# lower = more ocean coverage, higher = less water
WATER_THRESHOLD = 0.1
# lower = thinner beaches, higher = thicker coastal bands
BEACH_THRESHOLD = 0.2

# between mountain and normal terrain; defines hills
HILL_THRESHOLD = 0.72
# restrict building on hills
HILL_BUILDABLE = False
# lower = more mountains, higher = fewer and rarer peaks
MOUNTAIN_THRESHOLD = 0.78
# higher = sharper mountain peaks, lower = flatter elevation curves
SECONDARY_ELEVATION_WEIGHT = 0.35

# lower = more forest coverage, higher = more grassland instead
FOREST_MOISTURE_THRESHOLD = 0.65
# lower = more grassland in dry areas, higher = more desert
GRASSLAND_MOISTURE_THRESHOLD = 0.45

# higher = more grassland tiles turn into farmland
FARMLAND_CHANCE = 0.20
# higher = more dry grassland becomes desert
DESERT_CHANCE = 0.15

# rare chance hills contain gold
HILL_GOLD_CHANCE = 0.05
GOLD_EDGE_CHANCE = 0.25
# raise max for more gold per mountain tile
GOLD_MIN, GOLD_MAX = 1, 4
# increase for denser forest resource output
WOOD_MIN, WOOD_MAX = 3, 9
# higher = more productive farmland
FOOD_MIN, FOOD_MAX = 2, 5

# lower = smoother biome edges, higher = rougher/jagged transitions
BIOME_SMOOTHING_NOISE_SCALE = 0.05
# increase = larger saved map images, decrease = smaller previews
PREVIEW_TILE_SIZE = 2


class WorldGenerator:
    def __init__(self, grid_size, jitter=0.5, wavelength=0.5):
        self.grid_size = grid_size
        self.jitter = jitter
        self.wavelength = wavelength

        self.seed = random.randint(0, 999999)
        random.seed(self.seed)
        self.noise_seed = random.randint(0, 999999)

        self.points = self._generate_jittered_points()
        self.voronoi = Voronoi(self.points)
        self.kdtree = KDTree(self.points)

    def _generate_jittered_points(self):
        return np.array([
            [
                x + random.uniform(-self.jitter, self.jitter),
                y + random.uniform(-self.jitter, self.jitter)
            ]
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ])

    def _apply_smoothing(self, x, y):
        dx = snoise2(x * 0.5, y * 0.5, base=self.noise_seed +
                     100) * BIOME_SMOOTHING_NOISE_SCALE
        dy = snoise2(
            x * 0.5 + 100,
            y * 0.5 + 100,
            base=self.noise_seed + 200) * BIOME_SMOOTHING_NOISE_SCALE
        return x + dx, y + dy

    def _get_elevation(self, x, y):
        fx, fy = self._apply_smoothing(x, y)
        nx = fx / self.grid_size - 0.5
        ny = fy / self.grid_size - 0.5

        base = (1 + snoise2(nx / self.wavelength, ny /
                self.wavelength, base=self.noise_seed)) / 2
        sharp = (1 + snoise2(nx * 3, ny * 3, base=self.noise_seed + 300)) / 2
        combined = (1 - SECONDARY_ELEVATION_WEIGHT) * \
            base + SECONDARY_ELEVATION_WEIGHT * sharp

        d = 2 * max(abs(nx), abs(ny))
        return max(0.0, min(1.0, (1 + combined - d) / 2))

    def _get_moisture(self, x, y):
        fx, fy = self._apply_smoothing(x, y)
        nx = fx / self.grid_size - 0.5
        ny = fy / self.grid_size - 0.5
        m = (1 + snoise2((nx + 100) / self.wavelength, (ny + 100) /
             self.wavelength, base=self.noise_seed)) / 2
        return max(0.0, min(1.0, m))

    def _assign_biome(self, elevation, moisture):
        if elevation < WATER_THRESHOLD:
            return "water"
        elif elevation < BEACH_THRESHOLD:
            return "beach"
        elif elevation > MOUNTAIN_THRESHOLD:
            return "mountain"
        elif elevation > HILL_THRESHOLD:
            return "hill"
        elif moisture > FOREST_MOISTURE_THRESHOLD:
            return "forest"
        elif moisture > GRASSLAND_MOISTURE_THRESHOLD:
            # Favor farmland near wetter areas using noise-based clustering
            cluster_bias = snoise2(
                moisture * 10 + 200,
                elevation * 10 + 200,
                base=self.noise_seed
            )
            if cluster_bias > 0.2:
                return "farmland"
            else:
                return "grassland"
        elif moisture < 0.2:
            return "desert"
        else:
            return "grassland"

    def generate_tiles(self):
        tiles = []
        tile_map = {}

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                elevation = self._get_elevation(x, y)
                moisture = self._get_moisture(x, y)
                biome = self._assign_biome(elevation, moisture)

                resources = {}
                buildable = False

                if biome == "forest":
                    resources["wood"] = random.randint(WOOD_MIN, WOOD_MAX)
                elif biome == "farmland":
                    resources["food"] = random.randint(FOOD_MIN, FOOD_MAX)
                    buildable = True
                elif biome == "grassland":
                    buildable = True
                elif biome == "hill":
                    if random.random() < HILL_GOLD_CHANCE:
                        resources["gold"] = random.randint(GOLD_MIN, GOLD_MAX)
                    buildable = HILL_BUILDABLE

                tile = Tile(
                    x,
                    y,
                    biome,
                    elevation,
                    moisture,
                    resources,
                    buildable)
                tile_map[(x, y)] = tile
                tiles.append(tile)

        # Post-process for gold on mountain edges only
        for (x, y), tile in tile_map.items():
            if tile.biome != "mountain":
                continue

            neighbors = [
                tile_map.get((nx, ny))
                for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            ]
            if any(n is None or n.biome != "mountain" for n in neighbors):
                if random.random() < GOLD_EDGE_CHANCE:
                    tile.resources["gold"] = random.randint(GOLD_MIN, GOLD_MAX)

        print(
            "Tiles generated:",
            len(tiles),
            "Expected:",
            self.grid_size *
            self.grid_size)
        return tiles

    def generate_and_save(self):
        tiles = self.generate_tiles()
        json_path = self.save_to_file(tiles)
        return json_path

    def save_to_file(self, tiles):
        os.makedirs("save_data", exist_ok=True)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_data/new_world_{now}.json"
        data = {
            "width": self.grid_size,
            "height": self.grid_size,
            "seed": self.seed,
            "tiles": [tile.__dict__ for tile in tiles]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return filename
