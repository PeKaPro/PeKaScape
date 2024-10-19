"""
Module incorporating game items and its logic, food, weapons, factories for those...
"""
from random import choices
from typing import TYPE_CHECKING

from .base import ItemBase

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


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


class Food(ItemBase):
    """
    Food is some edible object that has a healing factor - it heals some health to a player
    """

    def __init__(self, name: str, room: 'MapFrame') -> None:
        super().__init__(name, room=room)

    @property
    def healing_factor(self) -> int:
        return FoodConfig.get_healing_factor(self.name)


class FoodFactory:

    @staticmethod
    def create_random(room: 'MapFrame') -> Food:
        food_name = choices(FoodConfig.FOOD_PROBS[0], FoodConfig.FOOD_PROBS[1])[0]
        return Food(name=food_name, room=room)
