"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""
import typing

if typing.TYPE_CHECKING:
    from pekascape.environment import MapFrame


class GameObject:

    def __init__(self, name, room: 'MapFrame'):
        self.name = name
        self.room = room

        self.room.add_content(self)


class Character(GameObject):

    def __init__(self, name: str, room: 'MapFrame', health: int, attack: int, defence: int):
        super().__init__(name, room)
        self.health = health
        self.attack = attack
        self.defence = defence

        self.items = list()

    def die(self) -> None:
        self.room.remove_content(self)
