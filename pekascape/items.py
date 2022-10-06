"""
Module incorporating game items and its logic, food, weapons, factories for those...
"""

from random import choices

import base
from environment import MapFrame


class FoodConfig:
    HEALING_FACTOR = {"Bread": 3,
                      "Apple": 1,
                      "Fish": 5}

    FOOD_PROBS = (
        ("Bread", "Apple", "Fish",),
        (0.3, 0.5, 0.2),
    )

    @staticmethod
    def get_healing_factor(food_identifier: str) -> int:
        return FoodConfig.HEALING_FACTOR.get(food_identifier, 0)


class Food(base.GameObject):
    """
    Food is some edible object that has a healing factor - it heals some health to a player
    """

    def __init__(self, name: str, room: MapFrame) -> None:
        super().__init__(name, room=room)

    @property
    def healing_factor(self) -> int:
        return FoodConfig.get_healing_factor(self.name)


class FoodFactory:

    @staticmethod
    def create_random(room: MapFrame) -> Food:
        food_name = choices(FoodConfig.FOOD_PROBS[0], FoodConfig.FOOD_PROBS[1])[0]
        return Food(name=food_name, room=room)


class WeaponConfig:
    MATERIALS_PROBS = (
        ("wood", "iron", "mithril",),
        (0.6, 0.3, 0.1),
    )

    MATERIAL_STRENGTH = {"wood": 3,
                         "iron": 10,
                         "mithril": 20,
                         }

    WEAPON_TYPES_PROBS = (
        ("dagger", "sword", "katana"),
        (0.5, 0.3, 0.2),
    )

    WEAPON_STRENGTH = {"dagger": 3,
                       "sword": 15,
                       "katana": 30}


class Weapon(base.GameObject):
    def __init__(self, room: MapFrame, material=None, weapon_type=None):
        super().__init__(name=f"{material} {weapon_type}", room=room)

        self.material = material
        self.weapon_type = weapon_type

        self.att_bonus = WeaponConfig.MATERIAL_STRENGTH[self.material] + WeaponConfig.WEAPON_STRENGTH[self.weapon_type]
        self.room.items.append(self)


class WeaponFactory:

    @staticmethod
    def create_random(room: MapFrame) -> Weapon:
        material = choices(WeaponConfig.MATERIALS_PROBS[0], WeaponConfig.MATERIALS_PROBS[1])[0]
        weapon_type = choices(WeaponConfig.WEAPON_TYPES_PROBS[0], WeaponConfig.WEAPON_TYPES_PROBS[1])[0]
        return Weapon(room, material, weapon_type)
