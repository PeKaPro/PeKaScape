import asyncio
import aioconsole


async def collect_input(input_queue: asyncio.Queue) -> None:
    while True:
        line = await aioconsole.ainput('What do you want to do next?:')
        await input_queue.put(line)


async def game_logic(input_queue: asyncio.Queue) -> None:
    print("I am alive")
    while True:
        if not input_queue.empty():
            key = await input_queue.get()
            print(f'You pressed: {key}')

        # Here you can put some calculations / actions
        print('Game advances.')
        await asyncio.sleep(1)  # Sleep to give the possibility for the other coroutine to execute.


async def main() -> None:
    input_queue: asyncio.Queue = asyncio.Queue(maxsize=1000)

    game_logic_coroutine = asyncio.create_task(game_logic(input_queue))
    collect_input_coroutine = asyncio.create_task(collect_input(input_queue))

    await asyncio.gather(game_logic_coroutine, collect_input_coroutine)

    print("I am done.")

asyncio.run(main())
