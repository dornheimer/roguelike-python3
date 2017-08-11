import libtcodpy as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    """Call input function depending on game state and return its result."""
    if game_state == GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in {GameStates.SHOW_INVENTORY, GameStates.SHOW_EQUIPMENT, GameStates.DROP_INVENTORY}:
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    return {}


def handle_player_turn_keys(key):
    """Define key bindings for the player's turn and return result of the key press."""
    key_char = chr(key.c)
    # Arrow keys and hjkl + numpad for diagonal movement
    if key.vk in {libtcod.KEY_UP, libtcod.KEY_KP8} or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk in {libtcod.KEY_DOWN, libtcod.KEY_KP2} or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk in {libtcod.KEY_LEFT, libtcod.KEY_KP4} or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk in {libtcod.KEY_RIGHT, libtcod.KEY_KP6} or key_char == 'l':
        return {'move': (1, 0)}
    elif key.vk == libtcod.KEY_KP1 or key_char == 'b':
        return {'move': (-1, 1)}
    elif key.vk == libtcod.KEY_KP3 or key_char == 'n':
        return {'move': (1, 1)}
    elif key.vk == libtcod.KEY_KP7 or key_char == 'z':
        return {'move': (-1, -1)}
    elif key.vk == libtcod.KEY_KP9 or key_char == 'n':
        return {'move': (1, -1)}
    elif key.vk in {libtcod.KEY_SPACE, libtcod.KEY_KP5}:
        return {'wait': True}

    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'e':
        return {'show_equipment': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    elif key.vk in {libtcod.KEY_ENTER, libtcod.KEY_KPENTER}:
        return {'take_stairs': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_targeting_keys(key):
    """Key bindings while targeting."""
    key_char = chr(key.c)

    if key.vk in {libtcod.KEY_UP, libtcod.KEY_KP8} or key_char == 'k':
        return {'select_target': (0, -1)}
    elif key.vk in {libtcod.KEY_DOWN, libtcod.KEY_KP2} or key_char == 'j':
        return {'select_target': (0, 1)}
    elif key.vk in {libtcod.KEY_LEFT, libtcod.KEY_KP4} or key_char == 'h':
        return {'select_target': (-1, 0)}
    elif key.vk in {libtcod.KEY_RIGHT, libtcod.KEY_KP6} or key_char == 'l':
        return {'select_target': (1, 0)}
    elif key.vk == libtcod.KEY_KP1 or key_char == 'b':
        return {'select_target': (-1, 1)}
    elif key.vk == libtcod.KEY_KP3 or key_char == 'n':
        return {'select_target': (1, 1)}
    elif key.vk == libtcod.KEY_KP5:
        return {'select_target': (0, 0)}
    elif key.vk == libtcod.KEY_KP7 or key_char == 'z':
        return {'select_target': (-1, -1)}
    elif key.vk == libtcod.KEY_KP9 or key_char == 'n':
        return {'select_target': (1, -1)}
    elif key.vk == libtcod.KEY_ENTER:
        return {'confirm': True}

    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    """Define key bindings for when the player is dead."""
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    """Define key bindings for the inventory menu."""
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_main_menu(key):
    """Define key bindings for the main menu."""
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_level_up_menu(key):
    """Define key bindings for level up menu."""
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}


def handle_character_screen(key):
    """Define key bindings for character screen."""
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    """Handle mouse input."""
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
