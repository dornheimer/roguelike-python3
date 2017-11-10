import libtcodpy as libtcod
from random import randint, random

from entity import Entity
from map_objects.dungeon_helper import Node, Rect
from map_objects.stairs import Stairs
from map_objects.tile import Tile
from render_functions import RenderOrder


class DunGen:
    """Base class for dungeon generation algorithms."""
    def __init__(self, width, height, dungeon_level):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]


class Rectangular:
    """
    Collection of methods that create and connect
    rectangular rooms in a dungeon.

    Can only be used as an 'addon' to the DunGen class.
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

    def create_stairs(self, entities):
        """Create stairs in last room."""
        center_last_room_x, center_last_room_y = self.rooms[-1].center()
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_last_room_x, center_last_room_y, '>', libtcod.lightest_grey, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)


class Tunnel(DunGen, Rectangular):
    """
    Create rectangular rooms of at random locations
    in the dungeon and connect them.

    The location and size of a room are chosen randomly (within bounds) and it
    will only be created if it does not overlap with previously created rooms.
    Rooms will connect to their previous room.
    """
    def __init__(self, width, height, room_min_size, room_max_size, dungeon_level):
        super().__init__(width, height, dungeon_level)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.rooms = []
        self.max_rooms = 30

    def create_dungeon(self, entities):
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

        self.create_stairs(entities)


class BSPTree(DunGen, Rectangular):
    """
    Recursively divide the area of the dungeon into sub areas and
    create rooms within them.
    """
    def __init__(self, width, height, room_min_size, room_max_size, dungeon_level):
        super().__init__(width, height, dungeon_level)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self._nodes = []
        self.max_node_size = 24
        self.rooms = []

    def create_dungeon(self, entities):
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

        self.create_stairs(entities)
