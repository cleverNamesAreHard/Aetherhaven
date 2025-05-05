# world/tile.py
class Tile:
    def __init__(
            self,
            x,
            y,
            biome,
            elevation,
            moisture,
            resources,
            buildable=True):
        self.x = x
        self.y = y
        self.biome = biome
        self.elevation = elevation
        self.moisture = moisture
        self.resources = resources or {}
        self.buildable = buildable

        self.occupied = False
        self.visible = True
