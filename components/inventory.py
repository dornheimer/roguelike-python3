import libtcodpy as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.equipment = []
        self.armor_equipped = False
        self.weapon_equipped = False

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), libtcod.blue)
            })

        self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message': Message('The {0} cannot be used'.format(item_entity))})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                libtcod.yellow)})

        return results

    def equip(self, item_entity, player):
        results = []

        item_component = item_entity.item

        attack = item_component.function_kwargs.get('attack')
        defense = item_component.function_kwargs.get('defense')
        item_name = item_component.function_kwargs.get('item_name')

        if item_component.equip:
            if defense:
                if self.armor_equipped:
                    results.append({'message': Message('You already have an armor equipped. Unequip first.')})
                    return results
                else:
                    player.fighter.defense += defense

                    self.remove_item(item_entity)
                    self.equipment.append(item_entity)
                    self.armor_equipped = True

            if attack:
                if self.weapon_equipped:
                    results.append({'message': Message('You already have a weapon equipped. Unequip first.')})
                    return results
                else:
                    player.fighter.power += attack

                    self.remove_item(item_entity)
                    self.equipment.append(item_entity)
                    self.weapon_equipped = True

            results.append({'equipped': True, 'message': Message(
                    'You have equipped the {0}'.format(item_name))})

        return results

    def unequip(self, item_entity, player):
        results = []

        item_component = item_entity.item

        attack = item_component.function_kwargs.get('attack')
        defense = item_component.function_kwargs.get('defense')
        item_name = item_component.function_kwargs.get('item_name')

        if defense and self.armor_equipped:
            player.fighter.defense -= defense

            self.items.append(item_entity)
            self.equipment.remove(item_entity)
            self.armor_equipped = False

        elif attack and self.weapon_equipped:
            player.fighter.power -= attack

            self.items.append(item_entity)
            self.equipment.append(item_entity)
            self.weapon_equipped = False


        results.append({'equipped': True, 'message': Message(
                'You have unequipped the {0}'.format(item_name))})

        return results
