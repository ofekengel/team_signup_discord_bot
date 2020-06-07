import asyncio
import time

import discord
from discord import Guild, Embed

from command_handlers.handler import Handler, CommandHandlerException
from db_api.storage_framework import TeamAlreadyExistException, PlayerAlreadyExistInAnotherRoleException
from db_api.team_members_db_api import PlayerAlreadyExistException
from model.leagues import LEAGUES
from model.player import Player


class PictureNotFoundException(Exception):
    pass


class StoreTeamCommandHandler(Handler):

    async def handle(self) -> Embed:
        try:
            logo = self.__get_team_picture()
            self.storage_framework.store_new_team(self.command.team, logo, self.command.team.team_tag)
            players = self.command.get_players()
            for player in players:
                self.storage_framework.store_new_player(player)
                await self.__add_role_to_player(player)
            return self.__create_result(logo)
        except PlayerAlreadyExistException as e:
            raise CommandHandlerException('<@{}> already exists'.format(e.args[0]))
        except TeamAlreadyExistException as e:
            raise CommandHandlerException('{} already exists'.format(e.args[0]))
        except PlayerAlreadyExistInAnotherRoleException as e:
            raise CommandHandlerException(
                '<@{}> is already in team {} as {}'.format(e.args[0].name, e.args[0].team_name, e.args[0].role))
        except PictureNotFoundException:
            raise CommandHandlerException('Please resign with a team logo')

    async def __add_role_to_player(self, player: Player) -> None:
        players_to_update = self.ctx.message.mentions
        role = None
        index = 0
        while role is None and index < 5:
            role = await self.__get_role_for_team(player.team_name)
            index += 1
        time.sleep(1)
        for player_to_update in players_to_update:
            if str(player_to_update.id) in player.name:
                await player_to_update.edit(
                    nick='{} {}'.format(self.command.team.team_tag.upper(), player_to_update.name))
                await player_to_update.add_roles(
                    discord.utils.get(self.ctx.server.roles, name='⁣         ^Team Roles^     ⁣'))
                await player_to_update.add_roles(role)
                await player_to_update.add_roles(
                    discord.utils.get(self.ctx.server.roles, name=LEAGUES[self.command.team.league.strip()]))

    async def __get_role_for_team(self, team_name):
        role = discord.utils.get(self.ctx.server.roles, name='Team | {}'.format(team_name))
        if role is not None:
            return role
        role_name = await self.__create_role_for_team(self.ctx.server)
        return discord.utils.get(self.ctx.server.roles, name=role_name)

    async def __create_role_for_team(self, server: Guild) -> str:
        role_name = 'Team | {}'.format(self.command.team.team_name)
        await server.create_role(name=role_name, hoist=True)
        return role_name

    def __get_team_picture(self) -> str:
        if len(self.ctx.message.attachments) > 0:
            return self.ctx.message.attachments[0].url
        raise PictureNotFoundException()

    def __create_result(self, logo: str):
        embed = self.command.get_representation()
        embed.set_thumbnail(url=logo)
        return embed
