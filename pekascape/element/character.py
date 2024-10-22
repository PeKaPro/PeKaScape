"""
Module defining basic agents of the game
1. Character as a very generic class
2. Player as a class meant to represent human player
3. Monster as a class of NPC enemies
"""

import typing

from ..behaviour.battle import BasicBattleEngine
from .base import GameObject, ItemsAccessMixin
from .food import Food
from .weapon import Weapon

if typing.TYPE_CHECKING:
    from pekascape.environment.environment import MapFrame


# todo: move printed texts into special enums in base modules


class Character(GameObject):
    """
    Represents basic agent in the game, either player or monster
    """

    def __init__(self, name: str, room: 'MapFrame', health: int, attack: int, defence: int):
        super().__init__(name, room)
        self.health = health
        self.attack = attack
        self.defence = defence

        self.items = []

    def die(self) -> None:
        self.room.remove_content(self)

    def __str__(self):
        return f"{type(self).__name__} {self.name} \n" \
               f"with attack {self.attack}, defence {self.defence} and {self.health} health"


class Player(Character, ItemsAccessMixin):
    """
    Player class - instance of this class is meant to be controlled by real world player
    """

    def __init__(self, name: str, room: 'MapFrame', health: int = 100, attack: int = 1, defence: int = 1):
        super().__init__(name, room, health, attack, defence)
        self.wielded_weapon = None

    @property
    def alive(self) -> bool:
        return self.health > 0

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
        if other not in self.room.characters_by_name:
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
        if item_name not in self.items_by_name:
            print("I cannot eat something I dont have")
            return

        item = self.get_item_by_name(item_name)
        if not isinstance(item, Food):
            print(f"I cannot eat {item_name}, it is not a food, it is a {type(item)}")

        self.items.remove(item)
        self.health += item.healing_factor  # TODO: LOL, you can increase health without limit...

    @property
    def total_attack(self) -> int:
        if self.wielded_weapon:
            return self.attack + self.wielded_weapon.att_bonus
        return self.attack

    def go(self, direction: str) -> None:  # pylint: disable=C0103
        target = self.room.neighbours.get(direction)
        if not target:
            print(f"There is no room in direction of {direction}.")
        else:
            target.characters.append(self)
            self.room.characters.remove(self)
            self.room = target
            self.see()

    def observe(self, monster_name: str) -> None:
        if monster_name not in self.room.characters_by_name:
            print(f"There is not monster named {monster_name} in this room")
        monster = self.room.get_character_by_name(monster_name)
        print(monster)


class Monster(Character):
    """
    Represents NPC enemy in the game
    """

    monster_count = 0

    @classmethod
    def track_count(cls) -> None:
        cls.monster_count += 1

    def __init__(self, room: 'MapFrame', health: int = 100, attack: int = 1, defence: int = 1):
        self.track_count()
        name = f"Monster{self.monster_count}"
        super().__init__(name, room, health, attack, defence)

    def fight(self, other: Character) -> None:
        pass

    def die(self) -> None:
        self.drop_items_on_death()
        super().die()

    def drop_items_on_death(self) -> None:
        while self.items:
            self.room.add_content(self.items.pop())