from team_members.player import Player


class Captain(Player):
    # def __init__(self, name: str, team_name: str, image_url):
    def __init__(self, name: str, team_name: str):
        # super().__init__(name, team_name, image_url)
        super().__init__(name, team_name)
        self.role = 'captain'
