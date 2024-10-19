"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class GameObject:

    def __init__(self, name: str, room: 'MapFrame'):
        self.name = name
        self.room = room

        self.room.add_content(self)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name} in {self.room}"
