from typing import Tuple

from db_api.db_communicator import DBCommunicator


class TeamsDBAPI:
    def __init__(self):
        self.__api = DBCommunicator('storage.db')
        self.__table_name = 'teams'

    def insert_team(self, team_name: str, team_logo: str = '', league: str = 'default') -> None:
        self.__api.execute_query(
            r"insert into {} values ('{}', '{}', '{}')".format(self.__table_name, team_name.replace("'", "''"), league,
                                                               team_logo))

    def get_team(self, team_name: str) -> Tuple:
        self.__api.execute_query(
            "select * from {} where team_name = {}".format(self.__table_name, team_name.replace("'", "''")))
        return self.__api.get_result()[0]

    def is_team_in_db(self, team_name: str) -> bool:
        self.__api.execute_query(
            "select * from {} where team_name = {}".format(self.__table_name, team_name.replace("'", "''")))
        if len(self.__api.get_result()) > 0:
            return True
        return False

    def __update_team_name(self, current_team_name, new_team_name: str, league: str = 'default') -> None:
        self.__api.execute_query(
            "update '{}' set team_name = '{}', league = '{}' where name = '{}'".format(self.__table_name, new_team_name,
                                                                                       league, current_team_name))
