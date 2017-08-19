import libtcodpy as libtcod

from game_messages import Message


class Equippable:
    """Component class for items that are equippable and their effects."""
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

    def __str__(self):
        boni = []
        if self.power_bonus:
            power = 'a%s' % self.power_bonus
            boni.append(power)
        if self.defense_bonus:
            defense = 'd%s' % self.defense_bonus
            boni.append(defense)
        if self.max_hp_bonus:
            max_hp = 'hp%s' % self.max_hp_bonus
            boni.append(max_hp)

        return " ".join(boni)
