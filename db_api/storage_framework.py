from sqlite3 import IntegrityError

from db_api.team_members_db_api import TeamMembersDBAPI, PlayerAlreadyExistException
from db_api.teams_db_api import TeamsDBAPI
from team_members.player import Player
from team_members.role_enum import RoleEnum


class PlayerNotRecognizedException(Exception):
    pass


class TeamAlreadyExistException(Exception):
    pass


class PlayerAlreadyExistInAnotherRoleException(Exception):
    pass


class PlayerNotInDBException(Exception):
    pass


class StorageFramework:
    def __init__(self):
        self.__player_storage_api = TeamMembersDBAPI()
        self.__team_storage_api = TeamsDBAPI()

    def store_new_player(self, player: Player) -> None:
        try:
            self.__player_storage_api.insert_player(player)
        except PlayerAlreadyExistException:
            existing_player = self.__player_storage_api.get_player(player.name)
            raise PlayerAlreadyExistInAnotherRoleException(existing_player)

    def store_new_team(self, team_name: str) -> None:
        try:
            self.__team_storage_api.insert_team(team_name)
        except IntegrityError as e:
            if 'UNIQUE' in e.args[0]:
                raise TeamAlreadyExistException(team_name)

    def are_players_in_the_same_team(self, player1: str, player2: str) -> bool:
        if not self.__player_storage_api.is_player_in_db(player1):
            raise PlayerNotRecognizedException()
        if not self.__player_storage_api.is_player_in_db(player2):
            raise PlayerNotRecognizedException()
        if self.__player_storage_api.get_player(player1).team_name == \
                self.__player_storage_api.get_player(player2).team_name:
            return True
        return False

    def get_player_data(self, player_name: str) -> Player:
        if not self.__player_storage_api.is_player_in_db(player_name):
            raise PlayerNotRecognizedException()
        return self.__player_storage_api.get_player(player_name)

    def update_role_for_player(self, player_name: str, role: RoleEnum) -> None:
        player_data = self.get_player_data(player_name)
        player_data.role = role.value
        self.__player_storage_api.update_player(player_data)

    def is_player_in_role(self, player_name: str, role: RoleEnum):
        return self.get_player_data(player_name).role == role.value

    def delete_player(self, player_name: str) -> None:
        if self.__player_storage_api.is_player_in_db(player_name):
            self.__player_storage_api.delete_player(player_name)
        raise PlayerNotInDBException()
