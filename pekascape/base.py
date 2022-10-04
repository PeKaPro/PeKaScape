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
