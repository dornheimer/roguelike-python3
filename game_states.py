from enum import Enum, auto

class GameStates(Enum):
    """Enum for game state variables."""
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
