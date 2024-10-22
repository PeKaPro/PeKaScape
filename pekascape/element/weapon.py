from random import choices
from typing import TYPE_CHECKING, Optional, Self

from pekascape.element.base import GameObject

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class Weapon(GameObject):
    """
    Represents weapon item in the game, material and type determine its strength
    """

    MATERIALS_PROBS = {
        "wood": 0.6,
        "iron": 0.3,
        "mithril": 0.1,
    }

    MATERIAL_STRENGTH = {
        "wood": 1,
        "iron": 5,
        "mithril": 10,
    }

    WEAPON_TYPES_PROBS = {
        "dagger": 0.5,
        "sword": 0.3,
        "katana": 0.2,
    }

    WEAPON_STRENGTH = {
        "dagger": 3,
        "sword": 15,
        "katana": 30
    }

    @classmethod
    def get_random_material(cls) -> str:
        return choices(
            list(cls.MATERIALS_PROBS.keys()),
            list(cls.MATERIALS_PROBS.values()),
        )[0]

    @classmethod
    def get_random_weapon_type(cls) -> str:
        return choices(
            list(cls.WEAPON_TYPES_PROBS.keys()),
            list(cls.WEAPON_TYPES_PROBS.values()),
        )[0]

    @classmethod
    def create_random(cls, room: 'MapFrame') -> Self:
        material = cls.get_random_material()
        weapon_type = cls.get_random_weapon_type()
        return cls(room, material, weapon_type)

    def __init__(self, room: 'MapFrame', material: Optional[str] = None, weapon_type: Optional[str] = None) -> None:
        super().__init__(name=f"{material} {weapon_type}", room=room)

        self.material = material
        self.weapon_type = weapon_type

        self.attack_bonus = self.MATERIAL_STRENGTH[self.material] + self.WEAPON_STRENGTH[self.weapon_type]
        self.room.items.append(self)
