import libtcodpy as libtcod
from random import randint

from components.ai import BasicMonster
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from entity import Entity
from game_messages import Message
from map_objects.items import consumables, equipment, max_items_dungeon, dagger, robes
from map_objects.monsters import max_monsters_dungeon, monsters
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from map_objects.stairs import Stairs
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class GameMap:
    """Contains methods for initializing tiles and creating rooms with monsters and items."""

    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        """Fill game map with blocked tiles."""
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        """Carve randomly generated rooms out of the game map."""
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # 'Rect' class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
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
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 1 or 0)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)

                # put entities into room
                self.place_entities(new_room, entities)

                # finally, append the new room to the list
                rooms.append(new_room)
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

    def create_item_entity(self, x, y, entity_data, is_equippable=False):
        """
        Create an item entity at specific coordinates on the game map.

        Item can be either consumable (default) or equippable.
        """
        item_component = None
        equippable_component = None

        if is_equippable:
            equippable_component = Equippable(**entity_data['kwargs'])
        else:
            item_component = Item(**entity_data['kwargs'])

        char, color, name = entity_data['entity_args']

        item_entity = Entity(x, y, char, color, name, render_order=RenderOrder.ITEM,
                                item=item_component, equippable=equippable_component, description=entity_data['description'])

        return item_entity

    def create_monster_entity(self, x, y, entity_data, equipment=None):
        """
        Create a monster entity at specific coordinates on the game map.

        Monster can have equipment (none by default).
        """
        fighter_component = Fighter(**entity_data['kwargs'])
        ai_component = BasicMonster()
        inventory_component = None
        equipment_component = None

        if equipment:
                inventory_component = Inventory((len(equipment)))
                equipment_component = Equipment()

        char, color, name = entity_data['entity_args']

        monster_entity = Entity(x, y, char, color, name, blocks=True,
                                render_order=RenderOrder.ACTOR, fighter=fighter_component,
                                ai=ai_component, inventory=inventory_component, equipment=equipment_component, description=entity_data['description'])

        if equipment:
            for item in equipment:
                equipment = self.create_item_entity(x, y, item, is_equippable=True)
                monster_entity.inventory.add_item(equipment)
                monster_entity.equipment.toggle_equip(equipment)

        return monster_entity

    def place_entities(self, room, entities):
        """Place a random number of monsters in each room of the map."""
        max_monsters_per_room = from_dungeon_level(max_monsters_dungeon, self.dungeon_level)
        max_items_per_room = from_dungeon_level(max_items_dungeon, self.dungeon_level)
        # Get a random number of monsters and items
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # Generate dictionary (elem -> chance ) for the appropriate dungeon level
        monster_chances = {m['id']: from_dungeon_level(m['spawn_chance'], self.dungeon_level) for m in monsters}
        consumables_chances = {c['id']: from_dungeon_level(c['drop_chance'], self.dungeon_level) for c in consumables}
        equipment_chances = {e['id']: from_dungeon_level(e['drop_chance'], self.dungeon_level) for e in equipment}

        ### Monsters
        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                for monster in monsters:
                    if monster_choice == monster['id']:
                        monster_entity = self.create_monster_entity(x, y, monster, monster['equipment'])

                entities.append(monster_entity)

        ### Items
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                select_item_pool = randint(0, 100)

                if select_item_pool < 70:
                    item_choice = random_choice_from_dict(consumables_chances)

                    for consumable in consumables:
                        if item_choice == consumable['id']:
                            item = self.create_item_entity(x, y, consumable)

                else:
                    item_choice = random_choice_from_dict(equipment_chances)

                    for equippable in equipment:
                        if item_choice == equippable['id']:
                            item = self.create_item_entity(x, y, equippable, is_equippable=True)

                entities.append(item)

    def is_blocked(self, x, y):
        """Return True if tile is blocked, otherwise False."""
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        """"Reset entities (except player) and generate a new dungeon floor."""
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                        constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
