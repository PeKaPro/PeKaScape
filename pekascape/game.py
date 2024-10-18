import random
from typing import Tuple

import pekascape.character.character as ch
import pekascape.environment.environment as en
import pekascape.item.items


class CustomGame:
    allowed_actions = ['see', 'go', 'fight', 'pickup', 'drop', 'wield', 'observe', 'stats', 'eat']

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
        self._populate_world()
        self._play()

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
            pekascape.item.items.WeaponFactory.create_random(room=self.map.random_frame)

        for i in range(int(self.food)):
            pekascape.item.items.FoodFactory.create_random(room=self.map.random_frame)

    @staticmethod
    def _collect_input() -> str:
        action = input('What do you want to do:')
        return action

    def _act_on_input(self, action: str) -> None:
        if not action:
            print("Try again, I dont understand what ", action, "means")

        if not action.startswith(tuple(self.allowed_actions)):
            print('sorry, I dont understand that \nAllowed actions are', ','.join(self.allowed_actions))

        action_mapping = {'go': self.player.go,
                          'fight': self.player.fight,
                          'pickup': self.player.pickup,
                          'drop': self.player.drop,
                          'wield': self.player.wield,
                          'observe': self.player.observe,
                          'eat': self.player.eat}

        if action == 'see':
            self.player.see()

        elif action == 'stats':
            print(self.player)

        else:
            action_parsed, subject = self._parse_action(action)
            print(action_parsed, subject)
            if action_method := action_mapping.get(action_parsed):
                action_method(subject)
            else:
                print("Try again, I dont understand what ", action, "means")

        # elif action.startswith('go'):
        #     self.player.go(self._get_subject(action))
        #
        # elif action.startswith('fight'):
        #     self.player.fight(self._get_subject(action))
        #
        # elif action.startswith('pickup'):
        #     self.player.pickup(self._get_subject(action))
        #
        # elif action.startswith('drop'):
        #     self.player.drop(self._get_subject(action))
        #
        # elif action.startswith('wield'):
        #     self.player.wield(self._get_subject(action))
        #
        # elif action.startswith('eat'):
        #     self.player.eat(self._get_subject(action))
        #
        # elif action.startswith('observe'):
        #     self.player.observe(self._get_subject(action))

    @staticmethod
    def _parse_action(action: str) -> Tuple[str, str]:
        instructions = action.split()
        return instructions[0], ' '.join(instructions[1:])

    def _play(self) -> None:
        while self.player.alive:
            self._act_on_input(self._collect_input())
