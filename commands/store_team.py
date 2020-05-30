from typing import List

import discord
from discord import Embed

from commands.icommand import ICommand
from team_members.captain import Captain
from team_members.team_member import TeamMember
from team_members.player import Player


class StoreTeam(ICommand):
    def __init__(self, team_name: str, captain: Captain, members: List[TeamMember]):
        self.team_name = team_name
        self.captain = captain
        self.members = members

    def get_players(self) -> List[Player]:
        players: List[Player] = self.members.copy()
        players.append(self.captain)
        return players

    def get_representation(self) -> Embed:
        embed = discord.Embed(title='Team name', description=self.team_name, color=discord.Color.from_rgb(255, 0, 42))
        embed.add_field(name='Captain', value='<@{}>'.format(self.captain.name), inline=False)
        members = ''
        for member in self.members:
            members += '<@{}>, '.format(member.name)
        members = members[:-2]
        embed.add_field(name='Members', value=members, inline=False)
        return embed
