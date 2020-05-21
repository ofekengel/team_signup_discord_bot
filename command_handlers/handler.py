from command_handlers.ctx import Ctx
from commands.icommand import ICommand


class CommandHandleException(Exception):
    pass


class Handler:
    def __init__(self, command: ICommand):
        self.command = command

    async def handle(self, ctx: Ctx) -> str:
        raise NotImplementedError()
