"""
Base module defining elements used by other modules

As it is newly created, things will be transferred here eventually

"""

from enum import Enum


class PlayerGameText(Enum):
    """
    Enum to encompass some game texts that are related to player
    """
    DEAD_INVOKE_ACTION = 'Dear, you are dead, give it up...'
