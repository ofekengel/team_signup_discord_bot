from typing import Tuple

from db_api.db_communicator import DBCommunicator
from team_members.player import Player


# todo: strings
class TeamMembersDBAPI:
    def __init__(self):
        self.__api = DBCommunicator('storage.db')
        self.__table_name = 'team_members'

    def insert_player(self, player: Player) -> None:
        self.__api.execute_query(
            "insert into {} values ('{}', '{}', '{}')".format(self.__table_name, player.name, player.role,
                                                              player.team_name))

    def get_player(self, player: Player) -> Tuple:
        # todo: add named tuple
        self.__api.execute_query("select * from {} where name = '{}'".format(self.__table_name, player.name))
        return self.__api.get_result()[0]

    def is_player_in_db(self, player: Player) -> bool:
        self.__api.execute_query(r"select * from {} where name = '{}'".format(self.__table_name, player.name))
        if len(self.__api.get_result()) > 0:
            return True
        return False

    def __update_player(self, player: Player):
        self.__api.execute_query(
            "update '{}' set role = '{}', team = '{}' where name = '{}'".format(self.__table_name, player.role,
                                                                                player.team_name, player.name))
