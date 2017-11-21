from random import randint

from map_objects.dungeon_components.rect import Rect
from map_objects.dungeon_generation.dun_gen import DunGen
from map_objects.dungeon_helper import Rectangular


class Tunnel(DunGen, Rectangular):
    """
    Create rectangular rooms of at random locations
    in the dungeon and connect them.
    """
    def __init__(self, width, height, room_min_size, room_max_size):
        super().__init__(width, height, noise=True)
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.rooms = []
        self.max_rooms = 50

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
            x = randint(0, self.width-w-1)
            y = randint(0, self.height-h-1)

            new_room = Rect(x, y, w, h)

            # Check if any of the other rooms intersects with this one
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                if num_rooms != 0:  # all rooms after the first
                    # Connect to the previous room with a tunnel
                    prev_room = self.rooms[num_rooms-1]
                    self.connect_rooms(new_room, prev_room)

                # Append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1

        self.apply_noise("water")
