import libtcodpy as libtcod

from map_objects.items import dagger, club

# maximum number of monsters per room [num, dungeon_level]
max_monsters_dungeon = [[2, 1], [3, 4], [5, 6]]

### BASIC AI MONSTERS ###
orc = {
    'id': 'orc',
    'entity_args': ('o', libtcod.desaturated_green, 'Orc'),
    'description':
        """This creature wields a sword and wears light armor.""",
    'equipment': [dagger],
    'spawn_chance': [[80, 1]],
    'kwargs': {
        'hp': 20,
        'defense': 0,
        'power': 3,
        'xp': 35
        }
    }

troll = {
    'id': 'troll',
    'entity_args': ('T', libtcod.darker_green, 'Troll'),
    'description':
        """This creature wields a heavy club and is protected my its thick skin.""",
    'equipment': [club],
    'spawn_chance':
        [[15, 3], [30, 5], [60, 7]],
    'kwargs': {
        'hp': 30,
        'defense': 2,
        'power': 8,
        'xp': 100
        }
    }

monsters = [
            orc,
            troll
            ]
