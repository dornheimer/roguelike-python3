import libtcodpy as libtcod

from random import randint


class Rectangular:
    """
    Collection of methods that create and connect
    rectangular rooms in a dungeon.

    Helper class that can only be used as an 'addon' to the DunGen class.
    """
    def create_room(self, room):
        """Go through the tiles in the rectangle and make them passable."""
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.tiles[x][y].carve()

    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel."""
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.tiles[x][y].carve()

    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel."""
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.tiles[x][y].carve()

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
            self.create_h_tunnel(x2, x1, y1)


def noise_2d(width, height):
    noise = libtcod.noise_new(2)
    noise_map = {}
    for x in range(width):
        for y in range(height):
            value = libtcod.noise_get(noise, [x*0.05, y*0.05])
            noise_map[(x, y)] = value * 50

    return noise_map
