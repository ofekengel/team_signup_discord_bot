from model.player import Player
from model.role_enum import RoleEnum


class TeamMember(Player):
    def __init__(self, name: str, team_name: str, profile_link: str):
        super().__init__(name, team_name, profile_link)
        self.role = RoleEnum.TEAM_MEMBER.value
