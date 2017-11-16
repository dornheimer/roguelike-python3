from map_objects.dungeon_components.tile import Tile


class DunGen:
    """Base class for dungeon generation algorithms."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]
