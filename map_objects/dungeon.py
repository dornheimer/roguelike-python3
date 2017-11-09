import libtcodpy as libtcod
from random import randint

from entity import Entity
from map_objects.stairs import Stairs
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder


class dunGen:
    def __init__(self, width, height, dungeon_level):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.tiles = self.initialize_tiles()
        self.rooms = []

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        """Return True if tile is blocked, otherwise False."""
        if self.tiles[x][y].blocked:
            return True

        return False


class Tunnel(dunGen):

    def create_dungeon(self, max_rooms, room_min_size, room_max_size, player, entities):
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(20, self.width - w - 1)
            y = randint(20, self.height - h - 1)

            # 'Rect' class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # 'paint' it to the map's tiles
                self.create_room(new_room)

                # center coordinates of the room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = self.rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 1 or 0)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)

                # finally, append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.lightest_grey, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

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
