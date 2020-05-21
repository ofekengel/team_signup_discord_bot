import discord
from discord import Guild

from command_hablers.ctx import Ctx
from command_hablers.handler import Handler, CommandHandleException
from commands.store_team import StoreTeam
from db_api.team_members_db_api import TeamMembersDBAPI
from db_api.teams_db_api import TeamsDBAPI
from team_members.player import Player
from sqlite3 import IntegrityError


class PlayerAlreadyExistException(Exception):
    pass


class TeamAlreadyExistException(Exception):
    pass


class PlayerAlreadyExistInAnotherRoleException(Exception):
    pass


class StoreTeamCommandHandler(Handler):
    def __init__(self, command: StoreTeam):
        super().__init__(command)
        self.__player_storage_api = TeamMembersDBAPI()
        self.__team_storage_api = TeamsDBAPI()

    async def handle(self, ctx: Ctx) -> str:
        try:
            self.__store_team()
            players = self.command.get_players()
            for player in players:
                self.__store_player(player)
                await self.__add_role_to_player(player, ctx)
            return self.command.get_representation()
        except PlayerAlreadyExistException as e:
            raise CommandHandleException('{} already exists'.format(e.args[0]))
        except TeamAlreadyExistException as e:
            raise CommandHandleException('{} already exists'.format(e.args[0]))
        except PlayerAlreadyExistInAnotherRoleException as e:
            raise CommandHandleException(
                '{} is already in team {} as {}'.format(e.args[0][0], e.args[0][2], e.args[0][1]))

    async def __add_role_to_player(self, player: Player, ctx: Ctx) -> None:
        players_to_update = ctx.message.mentions
        role_name = await self.__create_role_for_team(ctx.server)
        for player_to_update in players_to_update:
            if str(player_to_update.id) in player.name:
                role = discord.utils.get(ctx.server.roles, name=role_name)
                await player_to_update.add_roles(role)

    async def __create_role_for_team(self, server: Guild) -> str:
        role_name = 'Team | {}'.format(self.command.team_name)
        await server.create_role(name=role_name)
        return role_name

    def __store_player(self, player: Player) -> None:
        current_player_being_added = player.name
        try:
            if not self.__player_storage_api.is_player_in_db(player):
                self.__player_storage_api.insert_player(player)
            else:
                existing_player = self.__player_storage_api.get_player(player)
                raise PlayerAlreadyExistInAnotherRoleException(existing_player)
        except IntegrityError as e:
            if 'UNIQUE' in e.args[0]:
                raise PlayerAlreadyExistException(current_player_being_added)

    def __store_team(self) -> None:
        try:
            self.__team_storage_api.insert_team(self.command.team_name)
        except IntegrityError as e:
            if 'UNIQUE' in e.args[0]:
                raise TeamAlreadyExistException(self.command.captain.team_name)
