"""
Module incorporating food and other consumables and logic around it
"""
import base
from random import choices


# import threading - for future development of potions feature
# import time - likewise

_healing_factors = {"Bread": 3,
                    "Apple": 1,
                    "Fish": 5}


class Food(base.GameObject):
    def __init__(self, room=None):
        super().__init__(room=room)


class Bread(Food):
    def __init__(self, room=None):
        super().__init__(room)
        self.healing_factor = _healing_factors[type(self).__name__]

# potions - increases some stats temporarily





materials_probs = {10: "wood",
                   8: "iron",
                   5: "steel",
                   3: "mithril",
                   1: "adamant"}

materials = {"wood": 1,
             "iron": 5,
             "steel": 10,
             "mithril": 20,
             "adamant": 40}

weapon_types_probs = {10: "dagger",
                      6: "club",
                      4: "sword",
                      2: "scimitar"}

weapon_types = {"dagger": 3,
                "club": 5,
                "sword": 15,
                "scimitar": 30}


class Weapon(base.GameObject):
    def __init__(self, material = None, weapon_type = None, room = None):
        super().__init__(room)
        self.material = material if material is not None else choices(list(materials), list(materials_probs))[0]
        self.weapon_type = weapon_type if weapon_type is not None else choices(list(weapon_types), list(weapon_types_probs))[0]
        self.name = f"{self.material} {self.weapon_type}"
        self.att_bonus = materials[self.material] + weapon_types[self.weapon_type]
        self.room.items.append(self)


