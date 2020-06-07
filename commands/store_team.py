from typing import List

import discord
from discord import Embed

from commands.icommand import ICommand
from model.captain import Captain
from model.team import Team
from model.team_member import TeamMember
from model.player import Player


class StoreTeam(ICommand):
    def __init__(self, team: Team, captain: Captain, members: List[TeamMember]):
        self.team = team
        self.captain = captain
        self.members = members

    def get_players(self) -> List[Player]:
        players: List[Player] = self.members.copy()
        players.append(self.captain)
        return players

    def get_representation(self) -> Embed:
        embed = discord.Embed(title='Team name', description='{} {}'.format(self.team.team_name, self.team.team_tag), color=discord.Color.from_rgb(255, 0, 42))
        embed.add_field(name='League', value=self.team.league, inline=False)
        embed.add_field(name='Captain', value='<@{}>'.format(self.captain.name), inline=False)
        members = ''
        for member in self.members:
            members += '<@{}>, '.format(member.name)
        members = members[:-2]
        embed.add_field(name='Members', value=members, inline=False)
        return embed
