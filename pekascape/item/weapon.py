from random import choices
from typing import TYPE_CHECKING, Optional

from .base import ItemBase

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


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


class Weapon(ItemBase):
    def __init__(self, room: 'MapFrame', material: Optional[str] = None, weapon_type: Optional[str] = None) -> None:
        super().__init__(name=f"{material} {weapon_type}", room=room)

        self.material = material
        self.weapon_type = weapon_type

        self.att_bonus = WeaponConfig.MATERIAL_STRENGTH[self.material] + WeaponConfig.WEAPON_STRENGTH[self.weapon_type]
        self.room.items.append(self)


class WeaponFactory:

    @staticmethod
    def create_random(room: 'MapFrame') -> Weapon:
        material = choices(WeaponConfig.MATERIALS_PROBS[0], WeaponConfig.MATERIALS_PROBS[1])[0]
        weapon_type = choices(WeaponConfig.WEAPON_TYPES_PROBS[0], WeaponConfig.WEAPON_TYPES_PROBS[1])[0]
        return Weapon(room, material, weapon_type)
