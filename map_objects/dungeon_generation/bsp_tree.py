import random as rd

from map_objects.dungeon_components.node import Node
from map_objects.dungeon_generation.dun_gen import DunGen
from map_objects.dungeon_helper import Rectangular


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

    def create_dungeon(self):
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
                                    rd.random() > 0.8])
                    if try_split:
                        if n.split():
                            self._nodes.append(n.child_1)
                            self._nodes.append(n.child_2)
                            split_successfully = True

        root_node.create_rooms(self, self.room_min_size, self.room_max_size)
