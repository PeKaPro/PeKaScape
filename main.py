from game import GameEngine
import asyncio


async def main():
    g = GameEngine.create_small_game()
    await g.play()


if __name__ == '__main__':

    asyncio.run(main())


# TODO: add some drops from monster ... with some chance some random weapons and random food ...

# TODO: add hint for player

# TODO: add some prepared game
