import asyncio
import random
from typing import Self

from pekascape.element import Food, Monster, Player, Weapon
from pekascape.environment.environment import GridMap, Map
from pekascape.user_interface.user_control import UserControl


class GameEngine:
    """
    This should represent a custom game, but currently also serves as input-action parser
    # TODO: refactor this class, split it into input parser and game class
    """

    @classmethod
    def create_custom_game(cls) -> Self:
        print('hello there, you are starting new game of PeKaScape')
        player_name = input("please type in your name:")

        values = ["5*5", 50, 20, 20]
        for index, value in enumerate(['world size (in format of x*y)', 'monster count (int)', 'weapon count (int)', 'food count (int)']):
            values[index] = input(f"please, fill in the value for {value}:")

        world_size, monsters_count, weapons, food = values
        world_size = (int(x) for x in world_size.split('*'))

        world_map = GridMap(*world_size)

        # populate
        player = Player(name=player_name, room=world_map.random_tile, attack=20, defence=20)

        monsters = [Monster(room=world_map.random_tile, attack=random.randint(10, 50)) for _ in range(int(monsters_count))]

        for _ in range(int(weapons)):
            Weapon.create_random(room=world_map.random_tile)

        for _ in range(int(food)):
            Food.create_random(room=world_map.random_tile)

        return cls(player, world_map, monsters)

    @classmethod
    def create_small_game(cls) -> Self:
        world_map = GridMap(5, 5)
        player = Player(name='Peka', room=world_map.random_tile, attack=1, defence=1)

        monster_count, weapon_count, food_count = 20, 100, 5

        monsters = [Monster.get_random(room=world_map.random_tile) for _ in range(monster_count)]

        for _ in range(weapon_count):
            Weapon.create_random(room=world_map.random_tile)

        for _ in range(food_count):
            Food.create_random(room=world_map.random_tile)

        return cls(player, world_map, monsters)

    def __init__(self, player: Player, world_map: Map, monsters: list[Monster]) -> None:
        self.player = player
        self.world_map = world_map
        self.monsters = monsters

        self.command_queue = asyncio.Queue()
        self.command_semaphore = asyncio.Semaphore(1)
        self.control = UserControl(self.command_queue, self.command_semaphore)

    @staticmethod
    def _parse_action(action: str) -> tuple[str, str]:
        instructions = action.split()
        return instructions[0], ' '.join(instructions[1:])

    def _act_on_input(self, action: str) -> None:

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
            if not (action_method := action_mapping.get(action_parsed)):
                print("Try again, I dont understand what ", action, "means")
                return

            if subject:
                action_method(subject)
            else:
                action_method()

    async def play(self) -> None:
        control_collection_task = asyncio.create_task(self.control.collect_input())

        [asyncio.create_task(monster.act()) for monster in self.monsters]

        print("Game started")
        while self.player.alive:
            await self.play_turn()
        control_collection_task.cancel()

    async def play_turn(self) -> None:
        while True:
            if not self.command_queue.empty():
                action = await self.command_queue.get()

                async with self.command_semaphore:
                    self._act_on_input(action)

            await self.act()
            await asyncio.sleep(0.5)

    async def act(self) -> None:
        """
        This method should be called every turn and should be responsible for handling all the NPC actions
        """
