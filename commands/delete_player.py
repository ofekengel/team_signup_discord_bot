import discord

from commands.icommand import ICommand
from team_members.player import Player


class DeletePlayer(ICommand):

    def __init__(self, player: Player):
        self.player_to_delete = player

    def get_representation(self):
        embed = discord.Embed(title='player', description='<@{}>'.format(self.player_to_delete.name), color=discord.Color.from_rgb(255, 0, 42))
        return embed
