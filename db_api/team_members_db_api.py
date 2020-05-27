from typing import Tuple

from db_api.db_communicator import DBCommunicator
from team_members.player import Player


class PlayerAlreadyExistException(Exception):
    pass


# todo: strings
class TeamMembersDBAPI:
    def __init__(self):
        self.__api = DBCommunicator('storage.db')
        self.__table_name = 'team_members'

    def insert_player(self, player: Player) -> None:
        if self.is_player_in_db(player.name):
            raise PlayerAlreadyExistException()
        self.__api.execute_query(
            "insert into {} values ('{}', '{}', '{}')".format(self.__table_name, player.name, player.role,
                                                              player.team_name))

    def get_player(self, player_name: str) -> Player:
        # todo: add named tuple
        self.__api.execute_query("select * from {} where name = '{}'".format(self.__table_name, player_name))
        result = self.__api.get_result()[0]
        return Player(result[0], result[2], result[1])

    def is_player_in_db(self, player_name: str) -> bool:
        self.__api.execute_query(r"select * from {} where name = '{}'".format(self.__table_name, player_name))
        if len(self.__api.get_result()) > 0:
            return True
        return False

    def update_player(self, player: Player):
        self.__api.execute_query(
            "update '{}' set role = '{}', team = '{}' where name = '{}'".format(self.__table_name, player.role,
                                                                                player.team_name, player.name))
