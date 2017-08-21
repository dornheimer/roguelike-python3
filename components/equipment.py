from equipment_slots import EquipmentSlots


class Equipment:
    """Component class for equipment slots and the boni that their items provide."""

    def __init__(self, main_hand=None, off_hand=None, torso=None, head=None,
                    coat=None, ring_l=None, ring_r=None, special=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.torso = torso
        self.head = head
        self.coat = coat
        self.ring_l = ring_l
        self.ring_r = ring_r
        self.special = special

    @property
    def equipped(self):
        """List with all currently equipped items."""
        return [value for key, value in vars(self).items() if value and key != 'owner']

    @property
    def max_hp_bonus(self):
        """Calculate bonus to maximum hp from all equipped items."""
        bonus = 0

        for item in self.equipped:
            bonus += item.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        """Calculate bonus to power from all equipped items."""
        bonus = 0

        for item in self.equipped:
            bonus += item.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        """Calculate bonus to defense from all equipped items."""
        bonus = 0

        for item in self.equipped:
            bonus += item.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        """Equip / unequip item to the corresponding equipment slot."""
        results = []

        instance_variables = vars(self)
        slot = equippable_entity.equippable.slot

        for equipment_slot, enum in zip(instance_variables, EquipmentSlots):
            if slot == enum:
                # If item is already equipped, unequip it
                if instance_variables[equipment_slot] == equippable_entity:
                    setattr(self, equipment_slot, None)
                    results.append({'dequipped': equippable_entity})
                # Equip it otherwise
                else:
                    # Remove any previously equipped item
                    if instance_variables[equipment_slot]:
                        results.append({'dequipped': instance_variables[equipment_slot]})

                    setattr(self, equipment_slot, equippable_entity)
                    results.append({'equipped': equippable_entity})

                return results
