import random as rd

from map_objects.dungeon_components.rect import Rect
from map_objects.dungeon_components.tile import Tile
from map_objects.dungeon_generation.dun_gen import DunGen


class Buildings(DunGen):
    def __init__(self, width, height, room_min_size, room_max_size):
        super().__init__(width, height)
        self.tiles = self.initialize_tiles()
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_rooms = 7
        self.rooms = []
        self.distance = 4

    def initialize_tiles(self):
        """Fill game map with clear tiles."""
        return [[Tile(False) for y in range(self.height)] for x in range(self.width)]

    def create_dungeon(self, entities):
        for r in range(self.max_rooms):
            # Random width and height
            w = rd.randint(self.room_min_size, self.room_max_size)
            h = rd.randint(self.room_min_size, self.room_max_size)
            # Random position without going out of the boundaries of the map
            x = rd.randint(0, self.width-w-1)
            y = rd.randint(0, self.height-h-1)

            new_room = Rect(x, y, w, h)

            x_dist, y_dist = x-self.distance, y-self.distance,
            w_dist, h_dist = w+self.distance*2, h+self.distance*2
            area_around_room = Rect(x_dist, y_dist, w_dist, h_dist)

            # Check if any of the other rooms intersects with this one
            for other_room in self.rooms:
                if area_around_room.intersect(other_room):
                    break
            else:
                self.create_room_walls(new_room)
                self.exclude_from_spawning(new_room)

                # Append the new room to the list
                self.rooms.append(new_room)

    def create_room_walls(self, room):
        """Block tiles along the borders of the rectangle and create door."""
        wall_tiles = []
        for y in (room.y1, room.y2):
            for x in range(room.x1, room.x2+1):
                self.tiles[x][y].block()
                wall_tiles.append((x, y))

        for x in (room.x1, room.x2):
            for y in range(room.y1, room.y2+1):
                self.tiles[x][y].block()
                wall_tiles.append((x, y))

        # Prevent doorway in corners or too close to the edge
        door_locs = []
        for wt in wall_tiles:
            if wt[0] in (room.x1, room.x2):
                if room.y1+1 < wt[1] < room.y2-1:
                    door_locs.append(wt)
            elif wt[1] in (room.y1, room.y2):
                if room.x1+1 < wt[0] < room.x2-1:
                    door_locs.append(wt)
        doorway = rd.choice(door_locs)
        self.tiles[doorway[0]][doorway[1]].carve()

    def exclude_from_spawning(self, room):
        for x in range(room.x1, room.x2+1):
            for y in range(room.y1, room.y2+1):
                self.tiles[x][y].can_spawn = False
