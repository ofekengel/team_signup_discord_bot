import uuid

import discord
from discord import Guild, Embed

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.store_team import StoreTeam
from db_api.storage_framework import TeamAlreadyExistException, PlayerAlreadyExistInAnotherRoleException
from db_api.team_members_db_api import PlayerAlreadyExistException
from model.leagues import LEAGUES
from model.player import Player
from model.team import Team


class PictureNotFoundException(Exception):
    pass


class StoreTeamCommandHandler(Handler):
    def __init__(self, ctx: Ctx):
        super().__init__(ctx)

    async def handle(self, command: StoreTeam) -> Embed:
        try:
            logo = self.__get_team_picture()
            self.storage_framework.store_new_team(command.team, logo, command.team.team_tag)
            players = command.get_players()
            for player in players:
                self.storage_framework.store_new_player(player)
                await self.__add_role_to_player(player, command.team)
            return self.__create_result(logo, command)
        except PlayerAlreadyExistException as e:
            self.storage_framework.revert_changes()
            raise CommandHandlerException('<@{}> already exists'.format(e.args[0]))
        except TeamAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except PlayerAlreadyExistInAnotherRoleException as e:
            self.storage_framework.revert_changes()
            raise CommandHandlerException(
                '<@{}> is already in team {} as {}'.format(e.args[0].name, e.args[0].team_name, e.args[0].role))
        except PictureNotFoundException:
            raise CommandHandlerException('Please resign with a team logo')
        except Exception as e:
            self.storage_framework.revert_changes()
            error_id = uuid.uuid1()
            print('{}: {}'.format(error_id, e))
            raise CommandHandlerException(
                'oops something went wrong! please contact the technical team and send then the number  {}'.format(
                    error_id))

    async def __add_role_to_player(self, player: Player, team: Team) -> None:
        players_to_update = self.ctx.message.mentions
        # time.sleep(1)
        role = None
        for player_to_update in players_to_update:
            if str(player_to_update.id) in player.name:
                await player_to_update.edit(
                    nick='{} {}'.format(team.team_tag.upper(), player_to_update.name))
                await player_to_update.add_roles(
                    discord.utils.get(self.ctx.server.roles, name='⁣         ^Team Roles^     ⁣'))
                while role is None:
                    role = await self.__get_role_for_team(player.team_name)
                await player_to_update.add_roles(role)
                await player_to_update.add_roles(
                    discord.utils.get(self.ctx.server.roles, name=LEAGUES[team.league.strip()]))

    async def __get_role_for_team(self, team_name: str):
        role = discord.utils.get(self.ctx.server.roles, name='Team | {}'.format(team_name))
        if role is not None:
            return role
        role_name = await self.__create_role_for_team(self.ctx.server, team_name)
        return discord.utils.get(self.ctx.server.roles, name=role_name)

    @staticmethod
    async def __create_role_for_team(server: Guild, team_name: str) -> str:
        role_name = 'Team | {}'.format(team_name)
        await server.create_role(name=role_name, hoist=True)
        return role_name

    def __get_team_picture(self) -> str:
        if len(self.ctx.message.attachments) > 0:
            return self.ctx.message.attachments[0].url
        raise PictureNotFoundException()

    @staticmethod
    def __create_result(logo: str, command: StoreTeam):
        embed = command.get_representation()
        embed.set_thumbnail(url=logo)
        return embed
