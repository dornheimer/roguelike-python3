import libtcodpy as libtcod

from enum import Enum


class RenderOrder(Enum):
    """Render order in which entities will be drawn (highest last)."""
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def get_names_under_mouse(mouse, entities, fov_map):
    """Return name of entity if mouse is on top."""
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
                if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    """Draw health bar in bottom panel console."""
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE,
                            libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                screen_height, bar_width, panel_height, panel_y, mouse, colors):
    """Draw all tiles on the game (FOV) map and all entities in the list."""
    ### Game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                # Checks if tiles are in FOV
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        # libtcod.console_set_char_background(con, x, y, colors.get('light_wall'))
                        libtcod.console_put_char_ex(con, x, y, '#', libtcod.darker_han, libtcod.desaturated_azure)
                    else:
                        # libtcod.console_set_char_background(con, x, y, colors.get('light_ground'))
                        libtcod.console_put_char_ex(con, x, y, '.', libtcod.dark_grey, libtcod.darker_han)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        # libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'))
                        libtcod.console_put_char_ex(con, x, y, '#', libtcod.darkest_grey, libtcod.darkest_azure)
                    else:
                        # libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'))
                        libtcod.console_put_char_ex(con, x, y, '.', libtcod.darker_grey, libtcod.darkest_han)

    ### Entities
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(con, libtcod.black)

    ### Panel console
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the message, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1


    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
                libtcod.light_red, libtcod.darker_red)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                            get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)



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
