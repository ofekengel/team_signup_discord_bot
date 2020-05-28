from commands.icommand import ICommand
from team_members.player import Player


class AddPlayer(ICommand):
    def __init__(self, player_to_add: Player):
        self.player = player_to_add

    def get_representation(self) -> str:
        return 'Added player <@{}>'.format(self.player.name)
