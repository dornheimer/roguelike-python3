import libtcodpy as libtcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width,
                screen_height, colors):
    """Draws all tiles in the game (FOV) map and all entities in the list."""
    # Game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                # Checks if tiles are in FOV
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'))
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'))

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'))
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'))

    # Entities
    for entity in entities:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    """Erase characters of all entities."""
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    """Draw entity if it is in FOV."""
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """Erase the character that represents this object
    (prevents leaving a trail).
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
