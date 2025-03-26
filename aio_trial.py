import asyncio
import random
import threading


class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk=None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input())  # waits to get input + Return


def my_callback(inp):
    # evaluate the keyboard input
    print('You Entered:', inp, 'killing monster with that number...')
    x = [m for m in monsters if m.monster_count == int(inp)][0]
    x.alive = 0
    monsters.remove(x)


class Monster:
    monster_count = 0

    def __init__(self):
        Monster.monster_count += 1
        self.monster_count = Monster.monster_count
        self.name = f"Monster{self.monster_count}"
        self.alive = 1
        self.attack_lvl = random.randint(1, 10)
        self.coords = random.randint(1, 20)

    def attack(self, other):
        if self.attack_lvl > other.attack_lvl:
            other.alive = 0
            self.attack_lvl += other.attack_lvl

    async def activate(self):
        while self.alive:
            print(f"{self.name} - I am doing something...")
            print(f"{self.name} {self.monster_count}")
            await asyncio.sleep(random.randint(3, 15))
        print(f"I - {self.name} - am ending. the end. ")
        return


async def main(monsters):
    await asyncio.gather(*[m.activate() for m in monsters])


if __name__ == '__main__':
    kthread = KeyboardThread(my_callback)

    monsters = [Monster() for x in range(20)]

    asyncio.run(main(monsters))
