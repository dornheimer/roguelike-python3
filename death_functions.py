import libtcodpy as libtcod

from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
    """Player death.
    Change game state to PLAYER_DEAD and replace player with corpse.
    """
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    """Monster death.
    Replace monster with corpse and reset its attributes.
    """
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'The remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    monster.description = monster.name

    return death_message
