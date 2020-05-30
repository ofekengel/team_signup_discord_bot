from typing import Optional

from team_members.role_enum import RoleEnum


class Player:
    def __init__(self, name: str, team_name: str, profile_link: str, role: Optional[RoleEnum] = RoleEnum.EMPTY.value):
        self.name = name
        self.team_name = team_name
        self.profile_link = profile_link
        self.role = role
