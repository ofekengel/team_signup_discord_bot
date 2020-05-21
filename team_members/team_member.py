from team_members.player import Player
from team_members.role_enum import RoleEnum


class TeamMember(Player):
    # def __init__(self, name: str, team_name: str, image_url: str):
    def __init__(self, name: str, team_name: str):
        # super().__init__(name, team_name, image_url)
        super().__init__(name, team_name)
        self.role = RoleEnum.TEAM_MEMBER.value
