import libtcodpy as libtcod

### BASIC AI MONSTERS ###
orc = {
    'id': 'orc',
    'name':'Orc',
    'char': 'o',
    'color': libtcod.desaturated_green,
    'spawn_chance': 80,
    'kwargs': {
        'hp': 10,
        'defense': 0,
        'power': 3
        }
    }

troll = {
    'id': 'troll',
    'name':'Troll',
    'char': 'T',
    'color': libtcod.darker_green,
    'spawn_chance': 20,
    'kwargs': {
        'hp': 16,
        'defense': 1,
        'power': 4
        }
    }

monsters = [
            orc,
            troll
            ]
