import discord
from discord import Guild

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.store_team import StoreTeam
from db_api.team_members_db_api import TeamMembersDBAPI, PlayerAlreadyExistException
from db_api.teams_db_api import TeamsDBAPI
from team_members.player import Player
from sqlite3 import IntegrityError


class TeamAlreadyExistException(Exception):
    pass


class PlayerAlreadyExistInAnotherRoleException(Exception):
    pass


class StoreTeamCommandHandler(Handler):
    def __init__(self, command: StoreTeam, ctx: Ctx):
        super().__init__(command, ctx)
        self.__player_storage_api = TeamMembersDBAPI()
        self.__team_storage_api = TeamsDBAPI()

    async def handle(self) -> str:
        try:
            self.__store_team()
            players = self.command.get_players()
            for player in players:
                self.__store_player(player)
                await self.__add_role_to_player(player)
            return self.command.get_representation()
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

    def __store_player(self, player: Player) -> None:
        try:
            self.__player_storage_api.insert_player(player)
        except PlayerAlreadyExistException:
            existing_player = self.__player_storage_api.get_player(player.name)
            raise PlayerAlreadyExistInAnotherRoleException(existing_player)

    def __store_team(self) -> None:
        try:
            self.__team_storage_api.insert_team(self.command.team_name)
        except IntegrityError as e:
            if 'UNIQUE' in e.args[0]:
                raise TeamAlreadyExistException(self.command.captain.team_name)
