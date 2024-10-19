from typing import TYPE_CHECKING

from pekascape.base.base import GameObject

if TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


class ItemBase(GameObject):
    """
    Base class for all items in the game
    """

    def __init__(self, name: str, room: 'MapFrame') -> None:
        super().__init__(name, room=room)
