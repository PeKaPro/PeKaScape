from game import CustomGame
import asyncio


async def main():
    g = CustomGame()
    await g.play()


if __name__ == '__main__':

    asyncio.run(main())


# TODO: add some drops from monster ... with some chance some random weapons and random food ...

# TODO: add hint for player

# TODO: add some prepared game



