import libtcodpy as libtcod


# maximum number of monsters per room [num, dungeon_level]
max_monsters_dungeon = [[2, 1], [3, 4], [5, 6]]

### BASIC AI MONSTERS ###
orc = {
    'id': 'orc',
    'name':'Orc',
    'char': 'o',
    'color': libtcod.desaturated_green,
    'spawn_chance': [[80, 1]],
    'kwargs': {
        'hp': 20,
        'defense': 0,
        'power': 4,
        'xp': 35
        }
    }

troll = {
    'id': 'troll',
    'name':'Troll',
    'char': 'T',
    'color': libtcod.darker_green,
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
