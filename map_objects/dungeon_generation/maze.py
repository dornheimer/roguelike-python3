import random as rd

from map_objects.dungeon_components.rect import Rect
from map_objects.dungeon_generation.dun_gen import DunGen


class Maze(DunGen):
    """
    Python implimentation of the rooms and mazes algorithm found at
    http://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
    by Bob Nystrom

    === Original Description ===
    Starting with a stage of solid walls, it works like so:

    1. Place a number of randomly sized and positioned rooms. If a room
       overlaps an existing room, it is discarded. Any remaining rooms are
       carved out.
    2. Any remaining solid areas are filled in with mazes. The maze generator
       will grow and fill in even odd-shaped areas, but will not touch any
       rooms.
    3. The result of the previous two steps is a series of unconnected rooms
       and mazes. We walk the stage and find every tile that can be a
       "connector". This is a solid tile that is adjacent to two unconnected
       regions.
    4. We randomly choose connectors and open them or place a door there until
       all of the unconnected regions have been joined. There is also a slight
       chance to carve a connector between two already-joined regions, so that
       the dungeon isn't single connected.
    5. The mazes will have a lot of dead ends. Finally, we remove those by
       repeatedly filling in any open tile that's closed on three sides. When
       this is done, every corridor in a maze actually leads somewhere.

    The end result of this is a multiply-connected dungeon with rooms and lots
    of winding corridors.
    """
    north, south, east, west = (0, -1), (0, 1), (1, 0), (-1, 0)
    DIRECTIONS = [north, south, east, west]

    def __init__(self, width, height, room_min_size, room_max_size):
        super().__init__(width, height)
        self._regions = self._initialize_regions()

        self.rooms = []
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.build_room_attempts = 100
        self.extra_connector_chance = 0.04
        self.winding_percent = 0.2
        self.allow_dead_ends = False

    def _initialize_regions(self):
        """Associate every tile in the dungeon with a region (initially none).

        Maps every tile in the dungeon to the index of the connected region
        that that tile is a part of."""
        # Maze dimensions need to be odd
        if self.width % 2 == 0:
            self.mz_width = self.width - 1
        else:
            self.mz_width = self.width
        if self.height % 2 == 0:
            self.mz_height = self.height - 1
        else:
            self.mz_height = self.height

        # Index of the current region bring carved
        self._current_region = -1

        return [[None for y in range(self.mz_height)] for x in range(self.mz_width)]

    def create_dungeon(self, entities):
        self.add_rooms()

        # Fill in the empty space around the rooms with mazes
        for y in range(1, self.mz_height, 2):
            for x in range(1, self.mz_width, 2):
                if not self.tiles[x][y].blocked:
                    continue
                start = (x, y)
                self.grow_maze(start)

        self.connect_regions()

        if not self.allow_dead_ends:
            self.remove_dead_ends()

    def grow_maze(self, start):
        """Grow maze from <start> (randomized flood fill)."""
        cells = []
        last_direction = None

        self.start_region()
        self.carve_cell(start[0], start[1])

        cells.append(start)

        while len(cells):
            cell = cells[-1]

            # See if any adjacent cells are open
            unmade_cells = set()
            for direction in self.DIRECTIONS:
                if self.can_carve(cell, direction):
                    unmade_cells.add(direction)

            if len(unmade_cells):
                # Based on how "windy" passages are, try to prefer carving in
                # the same direction
                if (last_direction in unmade_cells) and (rd.random() > self.winding_percent):
                    direction = last_direction
                else:
                    direction = unmade_cells.pop()

                dx, dy = direction[0], direction[1]

                new_cell = ((cell[0]+dx), (cell[1]+dy))
                self.carve_cell(new_cell[0], new_cell[1])

                new_cell = ((cell[0]+dx*2), (cell[1]+dy*2))
                self.carve_cell(new_cell[0], new_cell[1])

                cells.append(new_cell)
                last_direction = direction

            else:
                # No adjacent uncarved cells
                del cells[-1]
                last_direction = None

    def add_rooms(self):
        """
        Pick random room size and random location.

        Ensure that rooms have odd sizes to properly align with the maze and
        prevent them from being to narrow or flat.
        """
        for i in range(self.build_room_attempts):
            w = rd.randint(self.room_min_size//2, self.room_max_size//2) * 2 + 1
            h = rd.randint(self.room_min_size//2, self.room_max_size//2) * 2 + 1
            x = (rd.randint(0, self.mz_width-w-1)//2) * 2 + 1
            y = (rd.randint(0, self.mz_height-h-1)//2) * 2 + 1

            new_room = Rect(x, y, w, h)

            # Check for overlap with any of the previous rooms
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.rooms.append(new_room)
                self.start_region()
                self.create_room(new_room)

    def connect_regions(self):
        """Find all the tiles that can connect two (or more) regions."""
        # Find all of the tiles that can connect two regions
        connector_regions = [[None for y in range(self.mz_height)]
                            for x in range(self.mz_width)]

        for x in range(1, self.mz_width-1):
            for y in range(1, self.mz_height-1):
                if not self.tiles[x][y].blocked:
                    continue

                # Count the number of different regions the wall tile is touching
                regions = set()
                for direction in self.DIRECTIONS:
                    new_x = x + direction[0]
                    new_y = y + direction[1]
                    region = self._regions[new_x][new_y]
                    if region is not None:
                        regions.add(region)

                # Tile must connect to least two regions
                if len(regions) >= 2:
                    connector_regions[x][y] = regions

        # Make a list of all the connectors
        connectors = set()
        for x in range(0, self.mz_width):
            for y in range(0, self.mz_height):
                if connector_regions[x][y]:
                    connector_position = (x, y)
                    connectors.add(connector_position)

        # Keep track of which regions have been merged. This maps an original
        # region index to the one it has been merged to.
        merged = {}
        open_regions = set()
        for i in range(self._current_region+1):
            merged[i] = i
            open_regions.add(i)

        # Connect the regions until one is left
        while len(open_regions) > 1:
            connector = rd.choice(tuple(connectors))  # Get random connector

            # Carve the connection
            self.add_junction(connector)

            # merge the connected regions
            x = connector[0]
            y = connector[1]

            # make a list of the regions at (x,y)
            regions = []
            for n in connector_regions[x][y]:
                # get the regions in the form of merged[n]
                actual_region = merged[n]
                regions.append(actual_region)

            dest = regions[0]
            sources = regions[1:]

            # Merge all of the affected regions. We have to look at ALL of the
            # regions because other regions may have been previously merged
            # with some of the ones we're merging now.
            for i in range(self._current_region+1):
                if merged[i] in sources:
                    merged[i] = dest

            # Clear the sources, they are no longer needed
            for source in sources:
                open_regions.remove(source)

            # Remove the unneeded connectors
            connectors_to_remove = set()
            for pos in connectors:
                # Remove connectors that are next to the current connector
                if self.distance(connector, pos) < 2:
                    connectors_to_remove.add(pos)
                    continue

                # Check if the connector still spans different regions
                regions = set()
                x = pos[0]
                y = pos[1]
                for n in connector_regions[x][y]:
                    actual_region = merged[n]
                    regions.add(actual_region)
                if len(regions) > 1:
                    continue

                # This connector isn't needed, but connect it occaisonally so
                # that the dungeon isn't singly-connected
                if rd.random() < self.extra_connector_chance:
                    self.add_junction(pos)

                if len(regions) == 1:
                    connectors_to_remove.add(pos)

            connectors.difference_update(connectors_to_remove)

    def create_room(self, room):
        """Carve rectangle into dungeon."""
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.carve_cell(x, y)

    def add_junction(self, pos):
        self.tiles[pos[0]][pos[1]].carve()

    def remove_dead_ends(self):
        done = False

        while not done:
            done = True

            for y in range(1, self.mz_height):
                for x in range(1, self.mz_width):
                    if not self.tiles[x][y].blocked:

                        # If it only has one exit, it's a dead end
                        exits = 0
                        for direction in self.DIRECTIONS:
                            dx, dy = direction[0], direction[1]
                            if not self.tiles[x+dx][y+dy].blocked:
                                exits += 1
                        if exits > 1:
                            continue

                        done = False
                        self.tiles[x][y].block()

    def can_carve(self, position, direction):
        """
        Gets whether or not an opening can be carved from the given starting
        cell at <position> to the adjacent cell facing <direction>.

        Returns True if the starting cell is in bounds and the destination cell
        is filled (or out of bounds).
        """
        x = position[0] + direction[0]*3
        y = position[1] + direction[1]*3

        # Must end in bounds
        if not (0 < x < self.mz_width) or not (0 < y < self.mz_height):
            return False

        x = position[0] + direction[0]*2
        y = position[1] + direction[1]*2

        # Destination must not be open
        return self.tiles[x][y].blocked

    def distance(self, loc1, loc2):
        return ((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2) ** 0.5

    def start_region(self):
        self._current_region += 1

    def carve_cell(self, x, y):
        self.tiles[x][y].carve()
        self._regions[x][y] = self._current_region
