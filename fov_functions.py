import libtcodpy as libtcod

def initialize_fov(game_map):
    """Returns a map that defines which tiles are lit."""
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                        not game_map.tiles[x][y].blocked)

    return fov_map
