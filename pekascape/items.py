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

    @staticmethod
    def get_healing_factor(food_identifier: str) -> int:
        return FoodConfig.HEALING_FACTOR.get(food_identifier, 0)


class Food(base.GameObject):
    """
    Food is some edible object that has a healing factor - it heals some health to a player
    """

    def __init__(self, room: MapFrame, healing_factor: int) -> None:
        super().__init__(room=room)
        self.healing_factor = healing_factor

    def _get_identifier(self) -> str:
        return type(self).__name__


class ConfigurableFood(Food):
    """
    This class works with FoodConfig class where the healing factors are managed in one place,
    child classes of ConfigurableFood further specialize 'behavior' only by defining their class name ...
    """

    def __init__(self, room: MapFrame) -> None:
        super().__init__(room, FoodConfig.get_healing_factor(self._get_identifier()))


class Bread(ConfigurableFood):
    ...


class Apple(ConfigurableFood):
    ...


class Fish(ConfigurableFood):
    ...


class WeaponConfig:
    MATERIALS_PROBS = (
        ("wood", "iron" "mithril",),
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
        super().__init__(room)

        self.material = material
        self.weapon_type = weapon_type

        self.att_bonus = WeaponConfig.MATERIAL_STRENGTH[self.material] + WeaponConfig.WEAPON_STRENGTH[self.weapon_type]
        self.room.items.append(self)

    @property
    def name(self) -> str:
        return f"{self.material} {self.weapon_type}"


class WeaponFactory:

    @staticmethod
    def create_random_weapon(room: MapFrame) -> Weapon:
        material = choices(WeaponConfig.MATERIALS_PROBS[0], WeaponConfig.MATERIALS_PROBS[1])[0]
        weapon_type = choices(WeaponConfig.WEAPON_TYPES_PROBS[0], WeaponConfig.WEAPON_TYPES_PROBS[1])[0]
        return Weapon(room, material, weapon_type)
