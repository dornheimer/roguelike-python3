import libtcodpy as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.dungeon import Tunnel, BSPTree
from map_objects.game_map import GameMap
from map_objects.items import dagger
from render_functions import RenderOrder


def get_constants():
    """Return game constants."""
    window_title = 'surprise_peach roguelike'

    # Window size
    screen_width = 80
    screen_height = 50

    # Panel
    panel_height = screen_height
    panel_width = 20
    panel_y = screen_height - panel_height
    panel_x = 0

    bar_width = 18

    message_x = 1
    message_width = panel_width - 2
    message_height = panel_height - 33

    # Map
    map_width = 80 - panel_width
    map_height = screen_height

    room_max_size = 10
    room_min_size = 6

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.black,
        'dark_wall_char': libtcod.Color(28, 5, 58), #libtcod.darkest_han,
        'dark_ground': libtcod.black,
        'dark_ground_char': libtcod.Color(49, 21, 87), #libtcod.darkest_azure,
        'light_wall': libtcod.black,
        'light_wall_char': libtcod.Color(83, 14, 83), #libtcod.desaturated_han,
        'light_ground': libtcod.black,
        'light_ground_char': libtcod.Color(138, 69, 138), #libtcod.desaturated_azure,
        'background_default': libtcod.black,
        'background_panel': libtcod.Color(31, 25, 89),
        'text_default': libtcod.lightest_sepia,
        'text_emphasize': libtcod.dark_orange,
        'text_desaturate': libtcod.lightest_sepia * libtcod.light_grey,
        'text_info': libtcod.light_han,
        'text_info_alt': libtcod.dark_magenta,
        'text_pickup': libtcod.darker_sky,
        'text_equip': libtcod.light_han,
        'text_unequip': libtcod.dark_magenta,
        'text_warning': libtcod.yellow,
        'text_target': None,
        'text_special': libtcod.light_yellow,
        'render_bar_fg': libtcod.darker_crimson,
        'render_bar_bg': libtcod.darker_red,
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_width': panel_width,
        'panel_x': panel_x,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors
    }

    return constants


def get_game_variables(constants):
    """Initialize game variables."""
    # === Entities ===
    fighter_component = Fighter(hp=100, defense=1, power=3)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcod.lightest_grey, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component, description='You.')
    entities = [player]

    equippable_component = Equippable(**dagger['kwargs'])
    char, color, name = dagger['entity_args']
    starting_weapon = Entity(0, 0, char, color, name, render_order=RenderOrder.ITEM,
                            equippable=equippable_component, description=dagger['description'])

    player.inventory.add_item(starting_weapon)
    player.equipment.toggle_equip(starting_weapon)

    # === Game map ===
    game_map = GameMap(constants['map_width'], constants['map_height'],
                        constants['room_min_size'], constants['room_max_size'])
    dungeon_type = Tunnel
    game_map.make_map(dungeon_type, player, entities)

    # === Message log ===
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    # === Game state ===
    game_state = GameStates.PLAYER_TURN

    return player, entities, game_map, message_log, game_state
