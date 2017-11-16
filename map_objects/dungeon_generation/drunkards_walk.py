from random import choices, randint, random

from map_objects.dungeon_components.rect import Rect
from map_objects.dungeon_generation.dun_gen import DunGen


class DrunkardsWalk(DunGen):
    """
    Move randomly to carve out a cave like area.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        self._percent_goal = 0.4
        self.walk_iterations = 25000  # Cut off in case _percent_goal is never reached
        self.weighted_toward_center = 0.15
        self.weighted_toward_prev_direction = 0.7
        self.zones = []

    @property
    def cleared(self):
        """List of coordinates that have been cleared."""
        cleared = []
        for x, col in enumerate(self.tiles):
            for y, tile in enumerate(col):
                if not tile.blocked:
                    cleared.append((x, y))
        return cleared

    def scan_for_zones(self):
        sections = []
        # divide map into min_room_size sized rectangles and check if they fit
        # in the dungeon layout
        w, h = 3, 3

        for x in range(0, self.width-w-1, w):
            for y in range(0, self.height-h-1, h):
                sections.append(Rect(x, y, w, h))

        for s in sections:
            section_tiles = [(x, y) for x in range(s.x1, s.x2) for y in range(s.y1, s.y2)]
            if all([st in self.cleared for st in section_tiles]):
                # 50% chance to make zone eligible for spawning
                if random() >= 0.5:
                    self.zones.append(s)

        print(len(self.zones))

    def create_dungeon(self, entities):
        """Walk until either goal or maximum iterations have been reached."""
        self.walk_iterations = max(self.walk_iterations, (self.width * self.height * 10))
        self._tiles_filled = 0
        self._prev_direction = None

        self.drunkard_x = randint(2, self.width - 2)
        self.drunkard_y = randint(2, self.height - 2)
        self.tiles_goal = self.width * self.height * self._percent_goal

        for i in range(self.walk_iterations):
            self.walk()
            if self._tiles_filled >= self.tiles_goal:
                break

        self.scan_for_zones()

    def walk(self):
        """
        Take a step into a random direction and unblock the destination tile.

        Directions' probability weights take into account map dimensions,
        if the current position is close to one of the edges and the
        direction of the previous step.
        """
        # === Choose direction ===
        # Increase probability of movement relative to map dimensions
        v_move = self.width / self.height
        h_move = self.height / self.width
        north, south, east, west = v_move, v_move, h_move, h_move

        # Weight the random walk against the edges
        if self.drunkard_x < self.width * 0.25:  # far left side of map
            east += self.weighted_toward_center
        elif self.drunkard_x > self.width * 0.75:  # far right side of map
            west += self.weighted_toward_center
        if self.drunkard_y < self.height * 0.25:  # top of the map
            south += self.weighted_toward_center
        elif self.drunkard_y > self.height * 0.75:  # bottom of the map
            north += self.weighted_toward_center

        # Weight in favor of the previous direction
        if self._prev_direction == "north":
            north += self.weighted_toward_prev_direction
        if self._prev_direction == "south":
            south += self.weighted_toward_prev_direction
        if self._prev_direction == "east":
            east += self.weighted_toward_prev_direction
        if self._prev_direction == "west":
            west += self.weighted_toward_prev_direction

        weights = [south, north, east, west]
        moves = {"south": (0, 1), "north": (0, -1), "east": (1, 0), "west": (-1, 0)}

        direction = choices(list(moves.keys()), weights)[0]
        dx, dy = moves[direction]

        # === Walk ===
        # check collision at edges
        if (1 < self.drunkard_x + dx < self.width - 1) and (1 < self.drunkard_y + dy < self.height - 1):
            self.drunkard_x += dx
            self.drunkard_y += dy
            if self.tiles[self.drunkard_x][self.drunkard_y]:
                self.tiles[self.drunkard_x][self.drunkard_y].blocked = False
                self.tiles[self.drunkard_x][self.drunkard_y].block_sight = False
                self._tiles_filled += 1
            self._prev_direction = direction
