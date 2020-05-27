from typing import Optional

from team_members.role_enum import RoleEnum


class Player:
    # def __init__(self, name: str, team_name: str, image_url: str):
    def __init__(self, name: str, team_name: str, role: Optional[RoleEnum] = RoleEnum.EMPTY.value):
        self.name = name
        self.team_name = team_name
        self.role = role
        # self.image_url = image_url
