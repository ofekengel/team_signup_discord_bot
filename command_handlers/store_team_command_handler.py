import discord
from discord import Guild

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.store_team import StoreTeam
from db_api.storage_framework import TeamAlreadyExistException, PlayerAlreadyExistInAnotherRoleException, \
    StorageFramework
from db_api.team_members_db_api import TeamMembersDBAPI, PlayerAlreadyExistException
from db_api.teams_db_api import TeamsDBAPI
from team_members.player import Player
from sqlite3 import IntegrityError


class StoreTeamCommandHandler(Handler):
    def __init__(self, command: StoreTeam, ctx: Ctx):
        super().__init__(command, ctx)
        self.__storage_framework = StorageFramework()

    async def handle(self) -> str:
        try:
            self.__storage_framework.store_new_team(self.command.team_name, self.ctx.message.attachments[0].url)
            players = self.command.get_players()
            for player in players:
                self.__storage_framework.store_new_player(player)
                await self.__add_role_to_player(player)
            return '{}\n{}'.format(self.ctx.message.attachments[0].url, self.command.get_representation())
        except PlayerAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except TeamAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except PlayerAlreadyExistInAnotherRoleException as e:
            raise CommandHandlerException(
                '{} is already in team {} as {}'.format(e.args[0].name, e.args[0].team_name, e.args[0].role))

    async def __add_role_to_player(self, player: Player) -> None:
        players_to_update = self.ctx.message.mentions
        role_name = await self.__create_role_for_team(self.ctx.server)
        for player_to_update in players_to_update:
            if str(player_to_update.id) in player.name:
                role = discord.utils.get(self.ctx.server.roles, name=role_name)
                await player_to_update.add_roles(role)

    async def __create_role_for_team(self, server: Guild) -> str:
        role_name = 'Team | {}'.format(self.command.team_name)
        await server.create_role(name=role_name)
        return role_name
