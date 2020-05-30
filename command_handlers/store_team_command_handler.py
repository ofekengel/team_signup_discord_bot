from typing import List

import discord
from discord import Guild, Embed

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.store_team import StoreTeam
from db_api.storage_framework import TeamAlreadyExistException, PlayerAlreadyExistInAnotherRoleException, \
    StorageFramework
from db_api.team_members_db_api import PlayerAlreadyExistException
from team_members.player import Player
from team_members.role_enum import RoleEnum


class PictureNotFoundException(Exception):
    pass


class StoreTeamCommandHandler(Handler):
    def __init__(self, command: StoreTeam, ctx: Ctx):
        super().__init__(command, ctx)
        self.__storage_framework = StorageFramework()

    async def handle(self) -> Embed:
        try:
            logo = self.__get_team_picture()
            self.__storage_framework.store_new_team(self.command.team_name, logo)
            players = self.command.get_players()
            for player in players:
                self.__storage_framework.store_new_player(player)
                await self.__add_role_to_player(player)
            return self.__create_result(players, logo)
        except PlayerAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except TeamAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except PlayerAlreadyExistInAnotherRoleException as e:
            raise CommandHandlerException(
                '{} is already in team {} as {}'.format(e.args[0].name, e.args[0].team_name, e.args[0].role))
        except PictureNotFoundException:
            raise CommandHandlerException('Please Upload a team logo')

    async def __add_role_to_player(self, player: Player) -> None:
        players_to_update = self.ctx.message.mentions
        role = await self.__get_role_for_team(player.team_name)
        for player_to_update in players_to_update:
            if str(player_to_update.id) in player.name:
                await player_to_update.add_roles(role)

    async def __get_role_for_team(self, team_name):
        role = discord.utils.get(self.ctx.server.roles, name='Team | {}'.format(team_name))
        if role is not None:
            return role
        role_name = await self.__create_role_for_team(self.ctx.server)
        return discord.utils.get(self.ctx.server.roles, name=role_name)

    async def __create_role_for_team(self, server: Guild) -> str:
        role_name = 'Team | {}'.format(self.command.team_name)
        await server.create_role(name=role_name)
        return role_name

    def __get_team_picture(self) -> str:
        if len(self.ctx.message.attachments) > 0:
            return self.ctx.message.attachments[0].url
        raise PictureNotFoundException()

    def __create_result(self, players: List[Player], logo: str):
        embed = discord.Embed(title='Team name', description=self.command.team_name, color=0x00ff00)
        embed.set_thumbnail(url=logo)
        for player in players:
            # todo: use Enum and not value
            if player.role == RoleEnum.CAPTAIN.value:
                embed.add_field(name='Captain', value='<@{}>'.format(player.name), inline=False)
            else:
                embed.add_field(name='Member', value='<@{}>'.format(player.name), inline=False)
        return embed
