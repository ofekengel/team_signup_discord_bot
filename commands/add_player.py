import discord

from commands.icommand import ICommand
from model.player import Player


class AddPlayer(ICommand):
    def __init__(self, player_to_add: Player):
        self.player = player_to_add

    def get_representation(self) -> discord.Embed:
        embed = discord.Embed(title='player added', description='<@{}>'.format(self.player.name), color=discord.Color.from_rgb(255, 0, 42))
        return embed
