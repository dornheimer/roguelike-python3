"""
Collection of dungeon generation algorithms that initialize map tiles and
carve out the dungeon layout.
"""
from random import choices, randint, random

from map_objects.dungeon_helper import Node, Rect
from map_objects.tile import Tile


class DunGen:
    """Base class for dungeon generation algorithms."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]

class Rectangular:
    """
    Collection of methods that create and connect
    rectangular rooms in a dungeon.

    Helper class that can only be used as an 'addon' to the DunGen class.
    """
    def create_room(self, room):
        """Go through the tiles in the rectangle and make them passable."""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def connect_rooms(self, room1, room2):
        """Connect two rooms with tunnels."""
        x1, y1 = room1.center()
        x2, y2 = room2.center()

        # 50% chance to carve horizontal tunnel first
        if randint(0, 1) == 1:
            self.create_h_tunnel(x2, x1, y2)
            self.create_v_tunnel(y2, y1, x1)
        else:
            # Move vertically first, then horizontally
            self.create_v_tunnel(y2, y1, x2)
            self.create_h_tunnel(x2, x1, y2)


class Tunnel(DunGen, Rectangular):
    """
    Create rectangular rooms of at random locations
    in the dungeon and connect them.
    """
    def __init__(self, width, height, room_min_size, room_max_size):
        super().__init__(width, height)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.rooms = []
        self.max_rooms = 30

    def create_dungeon(self, entities):
        """
        The location and size of a room are chosen randomly and it will only
        be created if it does not overlap with previously created rooms.
        Rooms will connect to their previous room,
        stairs will be placed in the last room.
        """
        num_rooms = 0
        for r in range(self.max_rooms):
            # Random width and height
            w = randint(self.room_min_size, self.room_max_size)
            h = randint(self.room_min_size, self.room_max_size)
            # Random position without going out of the boundaries of the map
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            # Check if any of the other rooms intersects with this one
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                if num_rooms != 0:  # all rooms after the first
                    # Connect to the previous room with a tunnel
                    prev_room = self.rooms[num_rooms - 1]
                    self.connect_rooms(new_room, prev_room)

                # Append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1


class BSPTree(DunGen, Rectangular):
    """
    Recursively divide the area of the dungeon into sub areas and
    create rooms within them.
    """
    def __init__(self, width, height, room_min_size, room_max_size):
        super().__init__(width, height)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self._nodes = []
        self.max_node_size = 24
        self.rooms = []

    def create_dungeon(self, entities):
        """
        Create root node of the tree and split recursively until nodes can no
        longer split. Carve out rooms in node areas and connect.
        Stairs are placed in the last room.
        """
        root_node = Node(0, 0, self.width, self.height)
        self._nodes.append(root_node)

        split_successfully = True
        # Loop through all leaves until they can no longer split successfully
        while split_successfully:
            split_successfully = False
            for n in self._nodes:
                if n.child_1 is None and n.child_2 is None:
                    try_split = any([n.width > self.max_node_size,
                                    n.height > self.max_node_size,
                                    random() > 0.8])
                    if try_split:
                        if n.split():
                            self._nodes.append(n.child_1)
                            self._nodes.append(n.child_2)
                            split_successfully = True

        root_node.create_rooms(self, self.room_min_size, self.room_max_size)


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
