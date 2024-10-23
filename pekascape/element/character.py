"""
Module defining basic agents of the game
1. Character as a very generic class
2. Player as a class meant to represent human player
3. Monster as a class of NPC enemies
"""
import asyncio
import random
from random import randint
from typing import TYPE_CHECKING, Optional, Self

from ..behaviour.battle import BasicBattleEngine
from .base import GameObject, ItemsAccessMixin
from .food import Food
from .weapon import Weapon

if TYPE_CHECKING:
    from pekascape.environment.environment import MapTile


# todo: move printed texts into special enums in base modules


class Character(GameObject):
    """
    Represents basic agent in the game, either player or monster
    """

    def __init__(self, name: str, room: 'MapTile', health: int, attack: int, defence: int):
        super().__init__(name, room)
        self.health = health
        self.attack = attack
        self.defence = defence

        self.items = []

    def die(self) -> None:
        self.room.remove_content(self)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name} with attack {self.attack}, defence {self.defence} and {self.health} health"

    @property
    def alive(self) -> bool:
        return self.health > 0

    def go(self, direction: str) -> None:  # pylint: disable=C0103
        target: Optional[MapTile] = self.room.neighbours.get(direction)
        if not target:
            print(f"There is no room in direction of {direction}.")
        else:
            target.characters.append(self)
            self.room.characters.remove(self)
            self.room = target


class Player(Character, ItemsAccessMixin):
    """
    Player class - instance of this class is meant to be controlled by real world player
    """

    def __init__(self, name: str, room: 'MapTile', attack: int = 1, defence: int = 1):
        self.max_health = health = 100

        super().__init__(name, room, health, attack, defence)
        self.wielded_weapon = None

    def __repr__(self) -> str:
        return f"{self.name} with attack {self.total_attack}, defence {self.defence} and {self.health} health"

    @property
    def fully_loaded(self) -> bool:
        return self.items == 3

    def pickup(self, item_name: str) -> None:

        if self.fully_loaded:
            print("I cant pick up anything, I am fully loaded.\nDrop something first")
            return

        if item_name not in self.room.items_by_name:
            print(f"I cant pick up {item_name} as its not in this room")
            return

        item = self.room.get_item_by_name(item_name)
        self.room.remove_content(item)
        self.items.append(item)

        print(f"I have picked up {item.name}.")
        if isinstance(item, Weapon):
            print(f"It has bonus {item.attack_bonus} - consider wielding it")

    def drop(self, item_name: str) -> None:
        if item_name not in self.items_by_name:
            print("I cant drop something I dont have, check your inventory again")
            return

        item = self.get_item_by_name(item_name)
        self.items.remove(item)
        self.room.add_content(item)

    def see(self) -> None:
        for direction in self.room.neighbours:
            if self.room.neighbours.get(direction):
                print(f"There is passage to the {direction}")

        for monster in self.room.monsters:
            print(f"There is {monster.name}")

        for item in self.room.items:
            print(f"There is {item.name} laying down")

    def fight(self, other: str) -> None:
        if other not in self.room.character_names:
            print(f"There is not monster named {other} in this room")
        else:
            print("Fight is on!")
            monster = self.room.get_character_by_name(other)
            BasicBattleEngine().fight(self, monster)

    def wield(self, item_name: str) -> None:
        if item_name not in self.items_by_name:
            print("I cannot wield something I dont have")
            return

        item = self.get_item_by_name(item_name)
        if not isinstance(item, Weapon):
            print(f"I cannot wield {item_name}, it is not a weapon, it is a {type(item)}")

        if self.wielded_weapon:
            print(f"I am wielding {self.wielded_weapon.name}, I will swap it with {item_name}")
            self.items.remove(item)
            self.items.append(self.wielded_weapon)
            self.wielded_weapon = item
        else:
            self.wielded_weapon = item
            self.items.remove(item)

    def eat(self, item_name: str) -> None:
        """
        Eating restores health, player can only eat food, health cannot exceed max_health
        """

        if item_name not in self.items_by_name:
            print("I cannot eat something I dont have")
            return

        item = self.get_item_by_name(item_name)
        if not isinstance(item, Food):
            print(f"I cannot eat {item_name}, it is not a food, it is a {type(item)}")

        self.items.remove(item)
        self.health = max([self.max_health, self.health + item.healing_factor])

    @property
    def total_attack(self) -> int:
        if self.wielded_weapon:
            return self.attack + self.wielded_weapon.att_bonus
        return self.attack

    def observe(self, monster_name: str) -> None:
        if monster_name not in self.room.character_names:
            print(f"There is not monster named {monster_name} in this room")
        monster = self.room.get_character_by_name(monster_name)
        print(monster)

    def go(self, direction: str) -> None:
        super().go(direction)
        self.see()


class Monster(Character):
    """
    Represents NPC enemy in the game
    """

    monster_count = 0

    CHANCE_ATTACK = 0.05
    CHANCE_MOVE = 0.1

    @classmethod
    def track_count(cls) -> None:
        cls.monster_count += 1

    @classmethod
    def get_random(cls, room: 'MapTile') -> Self:
        attack = randint(10, 50)
        return cls(room, attack)

    def __init__(self, room: 'MapTile', health: int = 100, attack: int = 1, defence: int = 1):
        self.track_count()
        name = f"Monster{self.monster_count}"
        super().__init__(name, room, health, attack, defence)

    def fight(self, other: Character) -> None:
        pass

    def die(self) -> None:
        self.drop_items()
        super().die()

    def drop_items(self) -> None:
        while self.items:
            self.room.add_content(self.items.pop())

    async def act(self) -> None:
        # attack player if in the same room with chance 20% +
        # move to another room with chance 10%

        while self.alive:
            await asyncio.sleep(2)
            await self._act_go()
            await self._act_fight()

    async def _act_fight(self) -> None:
        if random.random() < self.CHANCE_ATTACK:
            if character := self.room.get_player():
                BasicBattleEngine().fight(self, character)

    async def _act_go(self) -> None:
        if random.random() < self.CHANCE_MOVE:
            direction = random.choice(list(self.room.neighbours.keys()))
            self.go(direction)
