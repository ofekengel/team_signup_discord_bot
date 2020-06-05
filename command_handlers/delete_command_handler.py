import discord

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from command_handlers.update_player_command_handler import CouldNotAssignANewCaptain
from commands.delete_player import DeletePlayer
from db_api.storage_framework import StorageFramework, PlayerNotRecognizedException
from model.leagues import LEAGUES
from model.role_enum import RoleEnum


class DeleteCommandHandler(Handler):
    def __init__(self, command: DeletePlayer, ctx: Ctx):
        super().__init__(command, ctx)
        self.__storage_framework = StorageFramework()

    async def handle(self) -> str:
        try:
            if self.__storage_framework.is_player_in_role(self.ctx.message.author.id, RoleEnum.CAPTAIN):
                if self.__storage_framework.are_players_in_the_same_team(str(self.ctx.message.author.id), self.command.player_to_delete.name):
                    await self.remove_role()
                    self.__storage_framework.delete_player(self.command.player_to_delete.name)
                else:
                    raise CommandHandlerException('Cannot delete players in different teams')
                return self.command.get_representation()
            else:
                raise CommandHandlerException('Only captains are allowed to use this command')
        except PlayerNotRecognizedException:
            raise CommandHandlerException('Player not in a team')
        except CouldNotAssignANewCaptain:
            raise CommandHandlerException('You need to list a new captain within 1 minutes of the "update" command')

    async def remove_role(self):
        player = self.__storage_framework.get_player_data(self.command.player_to_delete.name)
        role = discord.utils.get(self.ctx.server.roles, name='Team | {}'.format(player.team_name))
        player_to_remove = self.ctx.message.mentions[0]
        team = self.__storage_framework.get_team_data_by_player(player)
        await player_to_remove.remove_roles(role)
        await player_to_remove.edit(nick='{}'.format(player_to_remove.name))

        await player_to_remove.remove_roles(
            discord.utils.get(self.ctx.server.roles, name='⁣         ^Team Roles^     ⁣'))
        await player_to_remove.remove_roles(role)
        await player_to_remove.remove_roles(
            discord.utils.get(self.ctx.server.roles, name=LEAGUES[team.league]))
