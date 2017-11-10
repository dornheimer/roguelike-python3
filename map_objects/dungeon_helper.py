from random import choice, randint, random


class Rect:
    """Rectangle specified by x, y coordinates and side lengths (w, h)."""

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        """Calculate center coordinates of a rectangle."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        """Return True if this rectangle intersects with another one."""
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Node:
    """Node in BSP Tree."""

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
            split_horizontally = choice([True, False])

        if split_horizontally:
            max_length = self.height - self.min_leaf_size
        else:
            max_length = self.width - self.min_leaf_size

        if max_length <= self.min_leaf_size:
            return False  # Node is too small to split further

        split = randint(self.min_leaf_size, max_length)

        if split_horizontally:
            self.child_1 = Node(self.x, self.y, self.width, split)
            self.child_2 = Node(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Node(self.x, self.y, split, self.height)
            self.child_2 = Node(self.x + split, self.y, self.width - split, self.height)

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
            w = randint(room_min_size, min(room_max_size, self.width - 1))
            h = randint(room_min_size, min(room_max_size, self.height - 1))
            x = randint(self.x, self.x + (self.width - 1) - w)
            y = randint(self.y, self.y + (self.height - 1) - h)

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
            elif random() < 0.5:
                return self.room_1
            else:
                return self.room_2
