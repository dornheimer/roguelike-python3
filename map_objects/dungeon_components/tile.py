class Tile:
    """
    A tile on a map.

    It may or may not be blocked, and may or may not block sight.
    Some tiles prevent spawning.
    """

    def __init__(self, blocked, block_sight=None, can_spawn=None):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

        # Spawning on a blocked tile is not possible
        if can_spawn is None:
            can_spawn = not blocked
        self.can_spawn = can_spawn

        self.explored = True

    def carve(self):
        self.blocked = False
        self.block_sight = False
        self.can_spawn = True

    def block(self):
        self.blocked = True
        self.block_sight = True
        self.can_spawn = False
