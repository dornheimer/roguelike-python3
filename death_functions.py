import libtcodpy as libtcod

from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
    """Player death.
    Change game state to PLAYER_DEAD and replace player with corpse.
    """
    player.char = '%'
    player.color = libtcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    """Monster death.
    Replace monster with corpse and reset its attributes.
    """
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ', + monster.name
    monster.RenderOrder = RenderOrder.CORPSE

    return death_message
