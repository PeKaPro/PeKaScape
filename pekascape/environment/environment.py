"""
Module to represent basic environment concepts
1. notion of physical space
    Basic class is MapFrame as a unit of space
    Map frames can be connected

"""
import abc
import random
from typing import Literal

from pekascape.element import Character, Monster
from pekascape.element.base import GameObject, ItemsAccessMixin

DIRECTION = Literal["north", "south", "east", "west"]


class MapFrame(ItemsAccessMixin):
    """
    Represents physical location, place where some interaction can happen.
    Player, items, monsters are in some location (MapFrame)
        and they can react to(with) each other if they are in the same MapFrame
    """

    def __init__(self, x_coord: int, y_coord: int) -> None:

        self.x_coord = x_coord
        self.y_coord = y_coord

        self.items = []
        self.characters: list[Character] = []

        self.neighbours = {}

    def set_adjacent_frame(self, direction: DIRECTION, adj_frame: 'MapFrame') -> None:
        self.neighbours[direction] = adj_frame

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x_coord, self.y_coord

    def remove_content(self, _object: GameObject) -> None:
        if _object in self.items:
            self.items.remove(_object)
            return
        if _object in self.characters:
            self.characters.remove(_object)
            return

    def add_content(self, subject: GameObject) -> None:
        if isinstance(subject, Character):
            self.characters.append(subject)
        else:
            self.items.append(subject)

    @property
    def character_names(self) -> list[str]:
        return [character.name for character in self.characters]

    def get_character_by_name(self, character_name: str) -> Character:
        return [character for character in self.characters if character.name == character_name][0]

    @property
    def monsters(self) -> list[Monster]:
        return [char for char in self.characters if isinstance(char, Monster)]


class Map(abc.ABC):
    """
    Generic class that represents game map - as a collection of map frames
    """

    def __init__(self) -> None:
        self.map_frames: list[MapFrame] = []

    @property
    def random_frame(self) -> MapFrame:
        return random.choice(self.map_frames)

    @abc.abstractmethod
    def _generate_map_frames(self) -> None:
        ...


class GridMap(Map):
    """
    Represents map as a grid of map frames
    """

    def __init__(self, size_x: int, size_y: int):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y

        self._index = {}

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
            self._index[map_frame.coordinates] = map_frame

    def _connect_map_frames(self) -> None:
        for map_frame in self.map_frames:
            x_coord, y_coord = map_frame.coordinates
            for direction, adjacent_map_frame in self._get_adjacent_frames(x_coord, y_coord):
                if not adjacent_map_frame:
                    continue
                map_frame.set_adjacent_frame(direction, adjacent_map_frame)

    def _get_adjacent_frames(self, x_coord: int, y_coord: int) -> tuple[DIRECTION, MapFrame]:
        directions = {
            "west": (-1, 0),
            "east": (1, 0),
            "south": (0, -1),
            "north": (0, 1)
        }

        for direction, (x_offset, y_offset) in directions.items():
            map_frame = self._index.get((x_coord + x_offset, y_coord + y_offset))
            if map_frame:
                yield direction, map_frame
