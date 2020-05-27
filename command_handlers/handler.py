from command_handlers.ctx import Ctx
from commands.icommand import ICommand


class CommandHandlerException(Exception):
    pass


class PlayerNotAuthorisedForThisCommandException(Exception):
    pass


class Handler:
    def __init__(self, command: ICommand, ctx: Ctx):
        self.ctx = ctx
        self.command = command

    async def handle(self) -> str:
        raise NotImplementedError()
