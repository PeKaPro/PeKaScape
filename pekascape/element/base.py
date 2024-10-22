"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class GameObject:
    """
    Basic class for all objects in the game, it has a name and a room it is in
    """

    def __init__(self, name: str, room: 'MapFrame'):
        self.name = name
        self.room = room

        self.room.add_content(self)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name} in {self.room}"


class ItemsAccessMixin:
    """
    Mixin for classes that have items
    """

    items: list[GameObject]

    @property
    def items_by_name(self) -> list[str]:
        return [item.name for item in self.items]

    def get_item_by_name(self, item_name: str) -> GameObject:
        return [item for item in self.items if item.name == item_name][0]
