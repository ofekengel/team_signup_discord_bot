from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from command_handlers.update_player_command_handler import CouldNotAssignANewCaptain
from commands.delete_player import DeletePlayer
from db_api.storage_framework import StorageFramework, PlayerNotRecognizedException
from team_members.role_enum import RoleEnum


class DeleteCommandHandler(Handler):
    def __init__(self, command: DeletePlayer, ctx: Ctx):
        super().__init__(command, ctx)
        self.__storage_framework = StorageFramework()

    async def handle(self) -> str:
        try:
            if self.__storage_framework.is_player_in_role(self.ctx.message.author.id, RoleEnum.CAPTAIN):
                if self.__storage_framework.are_players_in_the_same_team(self.ctx.message.author.id, self.command.player_to_delete.name):
                    self.__storage_framework.delete_player(self.command.player_to_delete.name)
                else:
                    raise CommandHandlerException('Cannot delete players in different teams')
                return self.command.get_representation()
            else:
                raise CommandHandlerException('Only captains are allowed to use this command')
        except PlayerNotRecognizedException:
            raise CommandHandlerException('Player not in in a team')
        except CouldNotAssignANewCaptain:
            raise CommandHandlerException('You need to list a new captain within 1 minutes of the "update" command')
