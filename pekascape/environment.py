"""
Module to represent basic environment concepts
1. notion of physical space
    Basic class is MapFrame as a unit of space
    Map frames can be connected


"""
import random
from typing import Literal, List, Tuple

DIRECTION = Literal["north", "south", "east", "west"]


class MapFrame:
    """This is the basic world element
    to incorporate the player-environment interaction"""

    # MapFrames = list()

    def __init__(self, x: int, y: int) -> None:
        # MapFrame.MapFrames.append(self)

        self.x = x
        self.y = y

        self.items = list()
        self.monsters = list()
        self.players = list()

        self.neighbours = dict()

    def set_adjacent_frame(self, direction: DIRECTION, adj_frame: 'MapFrame') -> None:
        self.neighbours[direction] = adj_frame

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y


class Map:
    """
    Generic class that represents game map - as a collection of map frames
    """

    def __init__(self) -> None:
        self.map_frames: List['MapFrame'] = []

    @property
    def random_frame(self):
        return random.choice(self.map_frames)


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

    def _get_adjacent_frames(self, x, y) -> Tuple[DIRECTION, MapFrame]:
        directions = {
            "west": (-1, 0),
            "east": (1, 0),
            "south": (0, -1),
            "north": (0, 1)
        }

        for direction, (adj_x, adj_y) in directions.items():
            mf = self._index.get(x + adj_x, y + adj_y)
            if mf:
                yield direction, mf
