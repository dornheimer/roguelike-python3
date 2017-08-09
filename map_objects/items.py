import libtcodpy as libtcod

from item_functions import heal, cast_confuse, cast_fireball, cast_freeze, cast_lightning
from game_messages import Message

### CONSUMABLES ###
targeting_message_color = libtcod.light_cyan

# Potions
healing_potion = {
    'id': 'healing_scroll',
    'name':'Healing Potion',
    'char': '!',
    'color': libtcod.violet,
    'drop_chance': 40,
    'kwargs': {
        'use_function': heal,
        'amount': 4
        }
    }

# Scrolls
confusion_scroll = {
    'id': 'confusion_scroll',
    'name':'Confusion Scroll',
    'char': '#',
    'color': libtcod.light_pink,
    'drop_chance': 10,
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
    'name':'Fireball Scroll',
    'char': '#',
    'color': libtcod.orange,
    'drop_chance': 15,
    'kwargs': {
        'use_function': cast_fireball,
        'targeting': True,
        'targeting_message': Message(
            'Left-click a target tile for the fireball or right-click to cancel.',
            targeting_message_color),
        'damage': 12,
        'radius': 2
        }
    }

freezing_scroll = {
    'id': 'freezing_scroll',
    'name':'Freezing Scroll',
    'char': '#',
    'color': libtcod.light_blue,
    'drop_chance': 15,
    'kwargs': {
        'use_function': cast_freeze,
        'targeting': True,
        'targeting_message': Message(
            'Left-click a target tile for the fireball or right-click to cancel.',
            targeting_message_color),
        'damage': 5,
        'radius': 1
        }
    }

lightning_scroll = {
    'id': 'lightning_scroll',
    'name':'Lightning Scroll',
    'char': '#',
    'color': libtcod.yellow,
    'drop_chance': 20,
    'kwargs': {
        'use_function': cast_lightning,
        'damage': 20,
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
# Armor
leather_armor = {
    'id': 'leather_armor',
    'name':'Leather Armor (1)',
    'char': '$',
    'color': libtcod.darker_amber,
    'drop_chance': 60,
    'kwargs': {
        'equip': True,
        'item_name':'Leather Armor (1)',
        'defense': 1
        }
    }
# Weapon
rusty_sword = {
    'id': 'rusty_sword',
    'name':'Rusty Sword [1]',
    'char': 'S',
    'color': libtcod.grey,
    'drop_chance': 40,
    'kwargs': {
        'equip': True,
        'item_name':'Rusty Sword [1]',
        'attack': 1
        }
    }
# Special

equipment = [
            leather_armor,
            rusty_sword
            ]
