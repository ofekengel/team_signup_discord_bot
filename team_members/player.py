from team_members.role_enum import RoleEnum


class Player:
    # def __init__(self, name: str, team_name: str, image_url: str):
    def __init__(self, name: str, team_name: str):
        self.name = name
        self.team_name = team_name
        self.role = RoleEnum.EMPTY.value
        # self.image_url = image_url
