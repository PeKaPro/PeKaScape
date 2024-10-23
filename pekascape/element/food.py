"""
Module incorporating game items and its logic, food, weapons, factories for those...
"""
from random import choices
from typing import TYPE_CHECKING, Self

from pekascape.element.base import GameObject

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class Food(GameObject):
    """
    Food is some edible object that has a healing factor - it heals some health to a player
    """

    HEALING_FACTOR = {
        "apple": 1,
        "bread": 3,
        "fish": 5,
    }

    FOOD_PROBS = {
        "apple": 0.5,
        "bread": 0.3,
        "fish": 0.2,
    }

    @classmethod
    def get_random_food(cls) -> str:
        return choices(
            list(cls.FOOD_PROBS.keys()),
            list(cls.FOOD_PROBS.values()),
        )[0]

    @classmethod
    def create_random(cls, room: 'MapFrame') -> Self:
        food_name = cls.get_random_food()
        return Food(name=food_name, room=room)

    def __init__(self, name: str, room: 'MapFrame') -> None:
        super().__init__(name, room=room)

    @property
    def healing_factor(self) -> int:
        return self.HEALING_FACTOR.get(self.name, 0)
