"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""
import typing

if typing.TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class GameObject:

    def __init__(self, name, room: 'MapFrame') -> None:
        self.name = name
        self.room = room

        self.room.add_content(self)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name} in {self.room}"

    def do(self, x):
        return x
