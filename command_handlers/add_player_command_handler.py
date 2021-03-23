import discord
from discord import Embed

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.add_player import AddPlayer
from db_api.storage_framework import PlayerNotRecognizedException
from model.leagues import LEAGUES
from model.player import Player
from model.role_enum import RoleEnum


class AddPlayerCommandHandler(Handler):
    def __init__(self, ctx: Ctx):
        super().__init__(ctx)

    async def handle(self, command: AddPlayer) -> Embed:
        try:
            if self.storage_framework.is_player_in_role(self.ctx.message.author.id, RoleEnum.CAPTAIN):
                if not self.storage_framework.is_player_signed(command.player.name):
                    self.__add_new_team_member(command.player)
                    await self.__add_role()
                else:
                    raise CommandHandlerException('Cannot add player that is already in a different team')
                return command.get_representation()
            else:
                raise CommandHandlerException('Only captains are allowed to use this command')
        except PlayerNotRecognizedException:
            raise CommandHandlerException('Player not in a team')

    def __add_new_team_member(self, player: Player):
        captain_data = self.storage_framework.get_player_data(self.ctx.message.author.id)
        player.team_name = captain_data.team_name
        self.storage_framework.store_new_player(player)

    async def __add_role(self):
        player = self.storage_framework.get_player_data(self.ctx.message.author.id)
        role = discord.utils.get(self.ctx.server.roles, name='Team | {}'.format(player.team_name))
        player_to_add = self.ctx.message.mentions[0]
        team = self.storage_framework.get_team_data_by_player(player)
        await player_to_add.edit(nick='{} {}'.format(team.team_tag.upper(), player_to_add.name))
        await player_to_add.add_roles(
            discord.utils.get(self.ctx.server.roles, name='⁣         ^Team Roles^     ⁣'))
        await player_to_add.add_roles(role)
        await player_to_add.add_roles(
            discord.utils.get(self.ctx.server.roles, name=LEAGUES[team.league]))
