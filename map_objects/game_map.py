"""
Handles dungeon generation and progression logic and places entities on the map.
"""
import libtcodpy as libtcod
import random as rd

from components.ai import BasicMonster
from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from entity import Entity
from game_messages import Message
from map_objects.dungeon_generation.bsp_tree import BSPTree
from map_objects.dungeon_generation.buildings import Buildings
from map_objects.dungeon_generation.drunkards_walk import DrunkardsWalk
from map_objects.dungeon_generation.maze import Maze
from map_objects.dungeon_generation.tunnel import Tunnel
from map_objects.items import consumables, equipment, max_items_dungeon
from map_objects.monsters import max_monsters_dungeon, monsters
from map_objects.stairs import Stairs
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class GameMap:
    """
    Methods for initializing tiles and creating rooms
    with monsters and items.
    """
    def __init__(self, width, height, room_min_size, room_max_size, dungeon_level=1):
        self.width = width
        self.height = height
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.dungeon_level = dungeon_level
        self.dungeon = None
        self.tiles = None

        self.dun_gens = {
            Tunnel: (self.width, self.height, self.room_min_size, self.room_max_size),
            BSPTree: (self.width, self.height, self.room_min_size, self.room_max_size),
            Buildings: (self.width, self.height, self.room_min_size, self.room_max_size),
            DrunkardsWalk: (self.width, self.height),
            Maze: (self.width, self.height, self.room_min_size, 10)
        }

    def is_blocked(self, x, y):
        """Return True if tile is blocked, otherwise False."""
        return self.dungeon.tiles[x][y].blocked

    def make_map(self, dungeon_type, player, entities):
        """Carve randomly generated rooms out of the game map."""
        parameters = self.dun_gens[dungeon_type]
        self.dungeon = dungeon_type(*parameters)
        self.dungeon.create_dungeon(entities)
        self.tiles = self.dungeon.tiles

        if dungeon_type in (BSPTree, Maze, Tunnel):
            # Put player in first room
            player.x, player.y = self.dungeon.rooms[0].center()

            # Put entities into every other room
            for room in self.dungeon.rooms[1:]:
                self.place_entities(room, entities)

            # Put stairs in last room
            center_last_room_x, center_last_room_y = self.dungeon.rooms[-1].center()
            self.place_stairs(center_last_room_x, center_last_room_y, entities)

        elif dungeon_type in (Buildings, DrunkardsWalk):
            # Choose player and stairs location at random
            player.x, player.y = rd.choice(self.dungeon.spawn_locations)
            stairs_x, stairs_y = rd.choice(self.dungeon.spawn_locations)
            # Make sure they are not at the same location
            while (stairs_x, stairs_y) == (player.x, player.y):
                stairs_x, stairs_y = rd.choice(self.dungeon.cleared)

            self.place_stairs(stairs_x, stairs_y, entities)

            if dungeon_type == DrunkardsWalk:
                for zone in self.dungeon.zones:
                    self.place_entities(zone, entities)

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
        number_of_monsters = rd.randint(0, max_monsters_per_room)
        number_of_items = rd.randint(0, max_items_per_room)
        # Generate dictionary (elem -> chance ) for the appropriate dungeon level
        monster_chances = {m['id']: from_dungeon_level(m['spawn_chance'], self.dungeon_level) for m in monsters}
        consumables_chances = {c['id']: from_dungeon_level(c['drop_chance'], self.dungeon_level) for c in consumables}
        equipment_chances = {e['id']: from_dungeon_level(e['drop_chance'], self.dungeon_level) for e in equipment}

        # === Monsters ===
        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = rd.randint(room.x1 + 1, room.x2 - 1)
            y = rd.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                for monster in monsters:
                    if monster_choice == monster['id']:
                        monster_entity = self.create_monster_entity(x, y, monster, monster['equipment'])

                entities.append(monster_entity)

        # === Items ===
        for i in range(number_of_items):
            x = rd.randint(room.x1 + 1, room.x2 - 1)
            y = rd.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                select_item_pool = rd.randint(0, 100)

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

    def place_stairs(self, x, y, entities):
        """Create stairs at coordinates."""
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(x, y, '>', libtcod.lightest_grey, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def next_floor(self, player, message_log, constants):
        """"Reset entities (except player) and generate a new dungeon floor."""
        self.dungeon_level += 1
        entities = [player]

        dungeon_type = rd.choice([BSPTree, DrunkardsWalk, Maze, Tunnel])
        self.make_map(dungeon_type, player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
