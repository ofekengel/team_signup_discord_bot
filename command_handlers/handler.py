from command_handlers.ctx import Ctx
from commands.icommand import ICommand
from db_api.storage_framework import StorageFramework


class CommandHandlerException(Exception):
    pass


class PlayerNotAuthorisedForThisCommandException(Exception):
    pass


class Handler:
    def __init__(self, command: ICommand, ctx: Ctx):
        self.ctx = ctx
        self.command = command
        self.storage_framework = StorageFramework(ctx.path)

    async def handle(self) -> str:
        raise NotImplementedError()
