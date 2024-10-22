import random

from pekascape.element import Food, Monster, Player, Weapon
from pekascape.environment.environment import GridMap


class CustomGame:
    """
    This should represent a custom game, but currently also serves as input-action parser
    # TODO: refactor this class, split it into input parser and game class
    """

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

    def _start_new(self) -> None:
        print('hello there, you are starting new game of PeKaScape')
        i = input("please type in your name:")
        self.player_name = i

    def _get_config(self) -> None:
        values = ["5*5", 50, 20, 20]
        for index, value in enumerate(['world size (in format of x*y)', 'monster count (int)', 'weapon count (int)', 'food count (int)']):
            values[index] = input(f"please, fill in the value for {value}:")

        self.world_size, self.monsters, self.weapons, self.food = values

    def _parse_config_values(self) -> None:
        self.world_size = (int(x) for x in self.world_size.split('*'))

    def _create_world(self) -> None:
        self.map = GridMap(*self.world_size)

    def _populate_world(self) -> None:

        self.player = Player(name=self.player_name, room=self.map.random_frame, health=500, attack=20, defence=20)
        for _ in range(int(self.monsters)):
            Monster(room=self.map.random_frame, attack=random.randint(10, 50))

        for _ in range(int(self.weapons)):
            Weapon.create_random(room=self.map.random_frame)

        for _ in range(int(self.food)):
            Food.create_random(room=self.map.random_frame)

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
    def _parse_action(action: str) -> tuple[str, str]:
        instructions = action.split()
        return instructions[0], ' '.join(instructions[1:])

    def play(self) -> None:
        while self.player.alive:
            self._act_on_input(self._collect_input())
