import os
import shelve

from map_objects.game_map import GameMap


def save_game(player, entities, game_map, message_log, game_state):
    """Save game to shelve file."""
    with shelve.open('savegame.dat') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


def load_game():
    """Load game from shelve file."""
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
