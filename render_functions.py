import libtcodpy as libtcod

from enum import Enum, auto
from game_states import GameStates
from menus import character_screen, equipment_menu, inventory_menu, level_up_menu


class RenderOrder(Enum):
    """Render order in which entities will be drawn (highest last)."""
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    """Return name of entity if mouse is on top."""
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
                if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    names = ', '.join(names)

    return names.capitalize()


def show_target(cursor, mouse, key, map_width, map_height, targeting_item):
    """Show target and impact radius (when applicable)."""
    (x, y) = (mouse.cx, mouse.cy)
    # Check if item component has a radius defined
    item_component = targeting_item.item
    radius = item_component.function_kwargs.get('radius')

    libtcod.console_clear(cursor)
    #libtcod.console_set_key_color(cursor, libtcod.black)

    if radius:
        for a in range(x - radius, x + radius + 1):
            for b in range(y - radius, y + radius + 1):
                libtcod.console_set_char_background(cursor, a, b, targeting_item.color)
    else:
        libtcod.console_set_char_background(cursor, x, y, libtcod.white)

    libtcod.console_blit(cursor, 0, 0, map_width, map_height, 0, 0, 0, 1.0, 0.5)


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


def render_info(panel, x, y, name, value, color):
    libtcod.console_set_default_foreground(panel, color)

    libtcod.console_print_ex(panel, x, y, libtcod.BKGND_NONE,
                            libtcod.LEFT, '{0}: {1}'.format(name, value))


def render_all(con, panel, cursor, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state, targeting_item, key):
    """
    Draw all tiles on the game (FOV) map and all entities in the list (con).
    Render panel and targeting (cursor) consoles.
    """
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
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('light_wall_char'), colors.get('light_wall'))
                    else:
                        # libtcod.console_set_char_background(con, x, y, colors.get('light_ground'))
                        libtcod.console_put_char_ex(con, x, y, '.', colors.get('light_ground_char'), colors.get('light_ground'))

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        # libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'))
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('dark_wall_char'), colors.get('dark_wall'))
                    else:
                        # libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'))
                        libtcod.console_put_char_ex(con, x, y, '.', colors.get('dark_ground_char'), colors.get('dark_ground'))

    ### Entities
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

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

    render_info(panel, 1, 2, 'Dungeon Level', game_map.dungeon_level, libtcod.light_sepia)
    render_info(panel, 1, 3, 'Attack', player.fighter.power, libtcod.lightest_grey)
    render_info(panel, 1, 4, 'Defense', player.fighter.defense, libtcod.lightest_grey)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                            get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in {GameStates.SHOW_INVENTORY, GameStates.SHOW_EQUIPMENT, GameStates.DROP_INVENTORY}:
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
            inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)
        elif game_state == GameStates.DROP_INVENTORY:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
            inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)
        else:
            inventory_title = 'Press the key next to an item to unequip it and move it back to inventory, or Esc to cancel.\n'
            equipment_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose at stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    elif game_state == GameStates.TARGETING:
        show_target(cursor, mouse, key, game_map.width, game_map.height, targeting_item)


def clear_all(con, entities):
    """Erase characters of all entities."""
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    """Draw entity if it is in FOV."""
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """Erase the character that represents this object
    (prevents leaving a trail).
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
