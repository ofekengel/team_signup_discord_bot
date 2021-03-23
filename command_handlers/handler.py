from command_handlers.ctx import Ctx
from commands.icommand import ICommand
from db_api.storage_framework import StorageFramework


class CommandHandlerException(Exception):
    pass


class PlayerNotAuthorisedForThisCommandException(Exception):
    pass


class Handler:

    def __init__(self, ctx: Ctx):
        self.ctx = ctx
        self.storage_framework = StorageFramework(ctx.path)

    async def handle(self, command: ICommand) -> str:
        raise NotImplementedError()
