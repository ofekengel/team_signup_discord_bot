from commands.icommand import ICommand
from team_members.player import Player


class DeletePlayer(ICommand):

    def __init__(self, player: Player):
        self.player_to_delete = player

    def get_representation(self):
        return 'deleted player <@{}>'.format(self.player_to_delete.name)
