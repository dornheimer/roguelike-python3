import libtcodpy as libtcod

from equipment_slots import EquipmentSlots
from item_functions import heal, cast_confuse, cast_fireball, cast_freeze, cast_lightning
from game_messages import Message


# maximum number of items per room [num, dungeon_level]
max_items_dungeon = [[1, 1], [2, 4]]

### CONSUMABLES ###
targeting_message_color = libtcod.light_cyan

# Potions
healing_potion = {
    'id': 'healing_scroll',
    'entity_args': ('!', libtcod.violet, 'Healing Potion'),
    'description':
        """A bottle holding a strange liquid.""",
    'drop_chance': [[35, 1]],
    'kwargs': {
        'use_function': heal,
        'amount': 40
        }
    }

# Scrolls
confusion_scroll = {
    'id': 'confusion_scroll',
    'entity_args': ('#', libtcod.light_pink, 'Confusion Scroll'),
    'description':
        """A Confusion Scroll.""",
    'drop_chance': [[10, 2]],
    'kwargs': {
        'use_function': cast_confuse,
        'targeting': True,
        'targeting_message': Message(
            'Left-click on an enemy to confuse it or right-click to cancel.',
            targeting_message_color)
        }
    }

fireball_scroll = {
    'id': 'fireball_scroll',
    'entity_args': ('#', libtcod.orange, 'Fireball Scroll'),
    'description':
        """A Fireball Scroll.""",
    'drop_chance': [[25, 6]],
    'kwargs': {
        'use_function': cast_fireball,
        'targeting': True,
        'targeting_message': Message(
            'Left-click a target tile for the fireball or right-click to cancel.',
            targeting_message_color),
        'damage': 25,
        'radius': 3
        }
    }

freezing_scroll = {
    'id': 'freezing_scroll',
    'entity_args': ('#', libtcod.light_blue, 'Freezing Scroll'),
    'description':
        """A Freezing Scroll.""",
    'drop_chance': [[15, 1]],
    'kwargs': {
        'use_function': cast_freeze,
        'targeting': True,
        'targeting_message': Message(
            'Left-click a target tile for the fireball or right-click to cancel.',
            targeting_message_color),
        'damage': 10,
        'radius': 1
        }
    }

lightning_scroll = {
    'id': 'lightning_scroll',
    'entity_args': ('#', libtcod.yellow, 'Lightning Scroll'),
    'description':
        """A Lightning Scroll.""",
    'drop_chance': [[25, 4]],
    'kwargs': {
        'use_function': cast_lightning,
        'damage': 40,
        'maximum_range': 5
        }
    }

consumables = [
                healing_potion,
                confusion_scroll,
                fireball_scroll,
                freezing_scroll,
                lightning_scroll
                ]

### Equipment ###
# Armor (torso)
leather_armor = {
    'id': 'leather_armor',
    'entity_args': ('(', libtcod.darker_amber, 'Leather Armor'),
    'description':
        """A worn leather armor.""",
    'drop_chance': [[40, 1]],
    'kwargs': {
        'slot': EquipmentSlots.TORSO,
        'defense_bonus': 2,
        }
    }

robes = {
    'id': 'robes',
    'entity_args': ('(', libtcod.light_sepia, 'Robes'),
    'description':
        """Thin cloth robes.""",
    'drop_chance': [[40, 1]],
    'kwargs': {
        'slot': EquipmentSlots.TORSO,
        'defense_bonus': 1,
        }
    }

# Armor (head)
leather_cap = {
    'id': 'leather_cap',
    'entity_args': ('(', libtcod.sepia, 'Leather Cap'),
    'description':
        """A thin leather cap.""",
    'drop_chance': [[30, 1]],
    'kwargs': {
        'slot': EquipmentSlots.HEAD,
        'defense_bonus': 1,
        }
    }

# Armor (coat)
cloth_cape = {
    'id': 'cloth_cape',
    'entity_args': ('(', libtcod.lighter_sepia, 'Cloth Cape'),
    'description':
        """A worn cloth cape.""",
    'drop_chance': [[20, 1]],
    'kwargs': {
        'slot': EquipmentSlots.COAT,
        'defense_bonus': 1,
        }
    }

# Armor (shield - off hand)
shield = {
    'id': 'shield',
    'entity_args': (')', libtcod.darker_orange, 'Shield'),
    'description':
        """A wooden shield.""",
    'drop_chance': [[15, 8]],
    'kwargs': {
        'slot': EquipmentSlots.OFF_HAND,
        'defense_bonus': 1
        }
    }
# Weapon (main hand)
dagger = {
    'id': 'dagger',
    'entity_args': ('-', libtcod.dark_sky, 'Dagger'),
    'description':
        """A small (and dull) dagger.""",
    'drop_chance': [[60, 1]],
    'kwargs': {
        'slot': EquipmentSlots.MAIN_HAND,
        'power_bonus': 1
        }
    }

rusty_sword = {
    'id': 'rusty_sword',
    'entity_args': ('/', libtcod.light_grey, 'Rusty Sword'),
    'description':
        """A rusty sword.""",
    'drop_chance': [[60, 1]],
    'kwargs': {
        'slot': EquipmentSlots.MAIN_HAND,
        'power_bonus': 3
        }
    }

# Special
health_amulet = {
    'id': 'health_amulet',
    'entity_args': ('§', libtcod.light_magenta, 'Health Amulet'),
    'description':
        """An amulet with a sparkling gem.""",
    'drop_chance': [[20, 1]],
    'kwargs': {
        'slot': EquipmentSlots.SPECIAL,
        'max_hp_bonus': 10
        }
    }

equipment = [
            leather_armor,
            robes,
            leather_cap,
            cloth_cape,
            shield,
            dagger,
            rusty_sword,
            health_amulet
            ]
