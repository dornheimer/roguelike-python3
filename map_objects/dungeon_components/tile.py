import json


with open("map_objects/dungeon_components/tiles.json") as tile_data:
    TILE_TYPES = json.load(tile_data)


class Tile:
    """
    A tile on a map.

    It may or may not be blocked, and may or may not block sight.
    Some tiles prevent spawning.
    """
    def __init__(self, tile_type="wall"):
        self._set_type(tile_type)
        self.explored = True

    def carve(self):
        self._set_type("ground")

    def block(self):
        self._set_type("wall")

    def _set_type(self, tile_type):
        self.tile_type = tile_type
        self.blocked = TILE_TYPES[tile_type]["blocked"]
        self.block_sight = TILE_TYPES[tile_type]["block_sight"]
        self.can_spawn = TILE_TYPES[tile_type]["can_spawn"]
        self.movement_mod = TILE_TYPES[tile_type]["movement_mod"]

        self.character = TILE_TYPES[tile_type]["character"]
        self.colors_dark = TILE_TYPES[tile_type]["colors_dark"]
        self.colors_lit = TILE_TYPES[tile_type]["colors_lit"]
