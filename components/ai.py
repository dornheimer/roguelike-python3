import libtcodpy as libtcod

from random import randint

from game_messages import Message


class BasicMonster:
    """Defines generic monster behaviour."""

    def take_turn(self, target, fov_map, game_map, entities):
        """Movement and attack during monster turn."""
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


class ConfusedMonster:
    """Monster behaviour when confused."""

    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        """Move randomly (or stay at position)."""
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results


class FrozenMonster:
    """Monster behaviour when frozen."""

    def __init__(self, previous_ai, number_of_turns=5):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        """Do not move until freezing effect wears off."""
        results = []

        if self.number_of_turns > 0:
            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer frozen!'.format(self.owner.name), libtcod.red)})

        return results
