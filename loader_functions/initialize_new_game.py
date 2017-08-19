import libtcodpy as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from map_objects.items import dagger
from render_functions import RenderOrder


def get_constants():
    window_title = 'deepglow roguelike'

    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.black,
        'dark_wall_char': libtcod.darkest_han,
        'dark_ground': libtcod.black,
        'dark_ground_char': libtcod.darkest_azure,
        'light_wall': libtcod.black,
        'light_wall_char': libtcod.desaturated_han,
        'light_ground': libtcod.black,
        'light_ground_char': libtcod.desaturated_azure,
        'text_pickup': None,
        'text_equip': None,
        'text_unequip': None,
        'text_warning': None,
        'text_target': None,
        'text_special': None
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors
    }

    return constants


def get_game_variables(constants):
        ### Entities
        fighter_component = Fighter(hp=100, defense=1, power=3)
        inventory_component = Inventory(26)
        level_component = Level()
        equipment_component = Equipment()
        player = Entity(0, 0, '@', libtcod.lightest_grey, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component, equipment=equipment_component, description='You.')
        entities = [player]

        equippable_component = Equippable(**dagger['kwargs'])
        char, color, name = dagger['entity_args']
        starting_weapon = Entity(0, 0, char, color, name, render_order=RenderOrder.ITEM, equippable=equippable_component, description=dagger['description'])

        player.inventory.add_item(starting_weapon)
        player.equipment.toggle_equip(starting_weapon)

        ### Game map
        game_map = GameMap(constants['map_width'], constants['map_height'])
        game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                            constants['map_width'], constants['map_height'], player, entities)

        ### Message log
        message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

        ### Game state
        game_state = GameStates.PLAYER_TURN

        return player, entities, game_map, message_log, game_state
