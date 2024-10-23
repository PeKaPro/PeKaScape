"""
Module to represent basic environment concepts
1. notion of physical space
    Basic class is MapTile as a unit of space
    Map frames can be connected

"""
import abc
import random
from typing import Literal, Optional

from element import Food, Weapon
from pekascape.element import Character, Monster, Player
from pekascape.element.base import GameObject, ItemsAccessMixin

DIRECTION = Literal["north", "south", "east", "west"]


class MapTile(ItemsAccessMixin):
    """
    Represents physical location, place where some interaction can happen.
    Player, items, monsters are in some location (MapTile)
        and they can react to(with) each other if they are in the same MapTile
    """

    def __init__(self, x_coord: int, y_coord: int) -> None:

        self.x_coord = x_coord
        self.y_coord = y_coord

        self.items = []
        self.characters: list[Character] = []

        self.neighbours = {}

    def set_adjacent_frame(self, direction: DIRECTION, adj_frame: 'MapTile') -> None:
        self.neighbours[direction] = adj_frame

    def get_player(self) -> Optional[Player]:
        for character in self.characters:
            if isinstance(character, Player):
                return character
        return None

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x_coord, self.y_coord

    def remove_content(self, _object: Character | Weapon | Food) -> None:
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

    def get_character_by_name(self, character_name: str) -> Character | None:
        for character in self.characters:
            if character.name == character_name:
                return character

    @property
    def monsters(self) -> list[Monster]:
        return [char for char in self.characters if isinstance(char, Monster)]


class Map(abc.ABC):
    """
    Generic class that represents game map - as a collection of map frames
    """

    def __init__(self) -> None:
        self.map_tiles: list[MapTile] = []

    @property
    def random_tile(self) -> MapTile:
        return random.choice(self.map_tiles)

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
                self.map_tiles.append(MapTile(i, j))

    def _index_map_frames(self) -> None:
        """
        Stores map frames of a world into an index structure - simple dict
        """
        for map_tile in self.map_tiles:
            self._index[map_tile.coordinates] = map_tile

    def _connect_map_frames(self) -> None:
        for map_tile in self.map_tiles:
            x_coord, y_coord = map_tile.coordinates
            for direction, adjacent_map_tile in self._get_adjacent_tiles(x_coord, y_coord):
                if not adjacent_map_tile:
                    continue
                map_tile.set_adjacent_frame(direction, adjacent_map_tile)

    def _get_adjacent_tiles(self, x_coord: int, y_coord: int) -> tuple[DIRECTION, MapTile]:
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
