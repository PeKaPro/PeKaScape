import asyncio

import aioconsole


class UserControl:
    _commands = {'see', 'go', 'fight', 'pickup', 'drop', 'wield', 'observe', 'stats', 'eat'}

    def __init__(self, command_queue: asyncio.Queue, command_semaphore: asyncio.Semaphore):
        self.command_queue = command_queue
        self.semaphore = command_semaphore

    def _is_command(self, command: str) -> bool:
        return command.startswith(tuple(self._commands))

    @property
    def commands(self) -> str:
        return ', '.join(self._commands)

    async def _collect_user_command(self) -> str | None:
        async with self.semaphore:
            command: str = await aioconsole.ainput('What do you want to do next?:')

            if not command:
                print("Empty command, try again")
                return

            if not self._is_command(command):
                print(f'Invalid command,\nAllowed commands are: {self.commands}')
                return

            return command

    async def collect_input(self) -> None:
        while True:
            command = await self._collect_user_command()
            if not command:
                continue

            async with self.semaphore:
                await self.command_queue.put(command)
                await asyncio.sleep(0.5)  # Sleep to give the possibility for the other coroutine
