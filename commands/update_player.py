from commands.icommand import ICommand
from team_members.player import Player
from team_members.role_enum import RoleEnum


class UpdatePlayer(ICommand):
    def __init__(self, player: Player, role: RoleEnum):
        self.player = player
        self.role = role

    def get_representation(self):
        return 'changed player <@{}> to role {}'.format(self.player.name, self.role.value)
