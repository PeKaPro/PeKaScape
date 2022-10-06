import random

import character as ch
import environment as en
import items


class Game:
    allowed_actions = ['see', 'go north', 'go south', 'go west', 'go east', 'fight']

    def __init__(self) -> None:
        self.world_size = None
        self.monsters = None
        self.weapons = None
        self.food = None

        self.world = None

        self._start_new()
        self._get_config()
        self._parse_config_values()
        self._create_world()

    def _start_new(self) -> None:
        print('hello there, you are starting new game of PeKaScape')
        i = input("please type in your name:")
        self.player_name = i

    def _get_config(self) -> None:
        values = list()
        for value in ['world size (in format of x*y)', 'monster count (int)', 'weapon count (int)', 'food count (int)']:
            values.append(input(f"please, fill in the value for {value}:"))

        self.world_size, self.monsters, self.weapons, self.food = values

    def _parse_config_values(self) -> None:
        self.world_size = (int(x) for x in self.world_size.split('*'))

    def _create_world(self) -> None:
        self.map = en.MazeMap(*self.world_size)

    def _populate_world(self) -> None:

        self.player = ch.Player(name=self.player_name, room=self.map.random_frame, health=500, attack=20, defence=20)
        for i in range(int(self.monsters)):
            ch.Monster(room=self.map.random_frame, attack=random.randint(10, 50))

        for i in range(int(self.weapons)):
            items.WeaponFactory.create_random(room=self.map.random_frame)

        for i in range(int(self.food)):
            items.FoodFactory.create_random(room=self.map.random_frame)

    @staticmethod
    def _collect_input() -> str:
        action = input('What do you want to do:')
        return action

    def _act_on_input(self, action: str) -> None:
        if action not in self.allowed_actions:
            print('sorry, I dont understand that \nAllowed actions are', ','.join(self.allowed_actions))

    def _play(self) -> None:
        while self.player.alive:
            self._act_on_input(self._collect_input())
