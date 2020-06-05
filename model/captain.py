from model.player import Player


class Captain(Player):
    def __init__(self, name: str, team_name: str, profile_link: str):
        super().__init__(name, team_name, profile_link)
        self.role = 'captain'
