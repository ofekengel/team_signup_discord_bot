from typing import List

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

    def get_representation(self) -> str:
        representation = 'Team is {}. Captain is <@{}>'.format(self.team_name, self.captain.name)
        if len(self.members) > 0:
            representation += ' members are'
            for member in self.members:
                representation += ' <@{}>'.format(member.name, member.role)
        else:
            representation += ' there are no members as of yet'
        return representation
