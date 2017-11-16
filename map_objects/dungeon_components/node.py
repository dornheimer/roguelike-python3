import random as rd

from map_objects.dungeon_components.rect import Rect


class Node:
    """
    Node in BSP Tree.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_leaf_size = 10
        self.child_1 = None
        self.child_2 = None
        self.room = None
        self.connected = []

    def split(self):
        """
        Split node into two children.

        If the width of the leaf is >25% larger than the height,
        split the leaf vertically.
        If the height of the leaf is >25% larger than the width,
        split the leaf horizontally.
        Otherwise, choose the direction at random.
        """
        # Check if node has already been split
        if self.child_1 is not None and self.child_2 is not None:
            return False

        # Determine direction of split
        if (self.width / self.height) >= 1.25:
            split_horizontally = False
        elif (self.height / self.width) >= 1.25:
            split_horizontally = True
        else:
            split_horizontally = rd.choice([True, False])

        if split_horizontally:
            max_length = self.height - self.min_leaf_size
        else:
            max_length = self.width - self.min_leaf_size

        if max_length <= self.min_leaf_size:
            return False  # Node is too small to split further

        split = rd.randint(self.min_leaf_size, max_length)

        if split_horizontally:
            self.child_1 = Node(self.x, self.y, self.width, split)
            self.child_2 = Node(self.x, self.y + split, self.width, self.height-split)
        else:
            self.child_1 = Node(self.x, self.y, split, self.height)
            self.child_2 = Node(self.x + split, self.y, self.width-split, self.height)

        return True

    def create_rooms(self, bsp_tree, room_min_size, room_max_size):
        """Follow branch and create rooms at the end nodes."""
        if self.child_1 or self.child_2:
            if self.child_1:
                self.child_1.create_rooms(bsp_tree, bsp_tree.room_min_size, bsp_tree.room_max_size)
            if self.child_2:
                self.child_2.create_rooms(bsp_tree, bsp_tree.room_min_size, bsp_tree.room_max_size)
            if self.child_1 and self.child_2:
                bsp_tree.connect_rooms(self.child_1.get_room(), self.child_2.get_room())

        else:
            # Create rooms in the end branches of the bsp tree
            w = rd.randint(room_min_size, min(room_max_size, self.width-1))
            h = rd.randint(room_min_size, min(room_max_size, self.height-1))
            x = rd.randint(self.x, self.x+(self.width-1)-w)
            y = rd.randint(self.y, self.y+(self.height-1)-h)

            self.room = Rect(x, y, w, h)
            bsp_tree.create_room(self.room)
            bsp_tree.rooms.append(self.room)

    def get_room(self):
        """
        Return room of node or recursively check its children
        and return one of their rooms instead.
        """
        if self.room:
            return self.room

        else:
            if self.child_1:
                self.room_1 = self.child_1.get_room()
            if self.child_2:
                self.room_2 = self.child_1.get_room()

            if not (self.child_1 and self.child_2):
                # neither room_1 nor room_2
                return None
            elif not self.room_2:
                # room_1 and !room_2
                return self.room_1
            elif not self.room_1:
                # room_2 and !room_1
                return self.room_2
            # If both rooms exist, pick one
            elif rd.random() < 0.5:
                return self.room_1
            else:
                return self.room_2
