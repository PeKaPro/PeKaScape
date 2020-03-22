"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""

from enum import Enum

from environment import MapFrame


class PlayerGameText(Enum):
    """
    Enum to encompass some game texts that are related to player
    """
    DEAD_INVOKE_ACTION = 'Dear, you are dead, give it up...'


class GameObject:
    game_objects = list()

    def __init__(self, room = None):
        if not MapFrame.MapFrames:
            MapFrame(1, 1)
            # This is to prevent creation of GameObjects before at least one MapFrame was instantiated.
        self.game_objects.append(self)
        self.room = room if room is not None else random.choice(MapFrame.MapFrames)