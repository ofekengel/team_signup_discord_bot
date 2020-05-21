from commands.icommand import ICommand
from team_members.role_enum import RoleEnum
from team_members.team_member import TeamMember


class UpdatePlayer(ICommand):
    def __init__(self, player: TeamMember, role: RoleEnum):
        self.player = player
        self.role = role
