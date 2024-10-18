"""
Module to represent basic environment concepts
1. notion of physical space
    Basic class is MapFrame as a unit of space
    Map frames can be connected


"""
import abc
import random
from typing import Literal, Union

from pekascape.base.base import GameObject
from pekascape.base.mixins import ItemsAccessMixin
from pekascape.character.character import Character
from pekascape.character.character import Monster

DIRECTION = Literal["north", "south", "east", "west"]


class MapFrame(ItemsAccessMixin):
    """
    Represents physical location, place where some interaction can happen.
    Player, items, monsters are in some location (MapFrame)
        and they can react to(with) each other if they are in the same MapFrame
    """

    def __init__(self, x: int, y: int) -> None:

        self.x = x
        self.y = y

        self.items = []
        self.characters: list[Character] = []

        self.neighbours = dict()

    def set_adjacent_frame(self, direction: DIRECTION, adj_frame: 'MapFrame') -> None:
        self.neighbours[direction] = adj_frame

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def remove_content(self, subject: Union[Character, GameObject]) -> None:
        if subject in self.items:
            self.items.remove(subject)
            return
        if subject in self.characters:
            self.characters.remove(subject)
            return

    def add_content(self, subject: Union[Character, GameObject]) -> None:
        if isinstance(subject, Character):
            self.characters.append(subject)
        else:
            self.items.append(subject)

    @property
    def characters_by_name(self) -> list[str]:
        return [character.name for character in self.characters]

    def get_character_by_name(self, character_name: str):
        return [character for character in self.characters if character.name == character_name][0]

    @property
    def monsters(self):
        return [char for char in self.characters if isinstance(char, Monster)]


class Map(abc.ABC):
    """
    Generic class that represents game map - as a collection of map frames
    """

    def __init__(self) -> None:
        self.map_frames: list['MapFrame'] = []

    @property
    def random_frame(self) -> MapFrame:
        return random.choice(self.map_frames)

    @abc.abstractmethod
    def _generate_map_frames(self) -> None:
        ...


class MazeMap(Map):

    def __init__(self, size_x: int = 5, size_y: int = 5):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y

        self._index = dict()
        self._generate_map_frames()
        self._index_map_frames()
        self._connect_map_frames()

    def _generate_map_frames(self) -> None:
        """
        Generates map frames and stores them into self
        """
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.map_frames.append(MapFrame(i, j))

    def _index_map_frames(self) -> None:
        """
        Stores map frames of a world into an index structure - simple dict
        """
        for map_frame in self.map_frames:
            self._index[map_frame.position] = map_frame

    def _connect_map_frames(self) -> None:
        for map_frame in self.map_frames:
            x, y = map_frame.position
            for direction, mf in self._get_adjacent_frames(x, y):
                if not mf:
                    continue
                map_frame.set_adjacent_frame(direction, mf)

    def _get_adjacent_frames(self, x, y) -> tuple[DIRECTION, MapFrame]:
        directions = {
            "west": (-1, 0),
            "east": (1, 0),
            "south": (0, -1),
            "north": (0, 1)
        }

        for direction, (adj_x, adj_y) in directions.items():
            mf = self._index.get((x + adj_x, y + adj_y))
            if mf:
                yield direction, mf
