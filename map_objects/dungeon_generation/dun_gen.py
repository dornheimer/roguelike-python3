from map_objects.dungeon_components.tile import Tile
from map_objects.dungeon_helper import noise_2d


class DunGen:
    """Base class for dungeon generation algorithms."""
    def __init__(self, width, height, noise=False):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        if noise:
            self.noise_map = noise_2d(width, height)

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        return [[Tile() for y in range(self.height)] for x in range(self.width)]

    @property
    def spawn_locations(self):
        return [(x, y) for x in range(self.width) for y in range(self.height) if self.tiles[x][y].can_spawn]

    def apply_noise(self, tile_type):
        for x in range(self.width):
            for y in range(self.height):
                n = self.noise_map[(x, y)]
                if abs(n) > 37 and (x, y) in self.spawn_locations:
                    self.tiles[x][y]._set_type(tile_type)
