class Fighter:
    """Fighter compomenent class for entities."""
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        self.hp -= amount

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            print('{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), target.name, str(damage)))
        else:
            print('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name))
