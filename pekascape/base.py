"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""
from pekascape.environment import MapFrame


class GameObject:
    game_objects = list()

    def __init__(self, room: MapFrame):
        self.game_objects.append(self)
        self.room = room

        if isinstance(self, Character):
            print('char')
            self.room.characters.append(self)
        else:
            self.room.items.append(self)


class Character(GameObject):

    def __init__(self, room: MapFrame, health: int = 100, attack: int = 1, defence: int = 1):
        # Character.Characters.append(self)
        super().__init__(room)
        self.health = health
        self.attack = attack
        self.defence = defence
