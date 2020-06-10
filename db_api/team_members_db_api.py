from db_api.db_communicator import DBCommunicator
from model.player import Player


class PlayerAlreadyExistException(Exception):
    pass


# todo: strings; decorate escaping
class TeamMembersDBAPI:
    def __init__(self, path: str):
        self.__api = DBCommunicator(path + 'storage.db')
        self.__table_name = 'team_members'

    def insert_player(self, player: Player) -> None:
        if self.is_player_in_db(player.name):
            raise PlayerAlreadyExistException()
        self.__api.execute_query(
            "insert into {} values ('{}', '{}', '{}', '{}')".format(self.__table_name, str(player.name).replace("'", "''"), player.role,
                                                              player.team_name.replace("'", "''"), player.profile_link))

    def get_player(self, player_name: str) -> Player:
        # todo: add named tuple
        self.__api.execute_query("select * from {} where name = '{}'".format(self.__table_name, str(player_name).replace("'", "''")))
        result = self.__api.get_result()[0]
        return Player(name=result[0], role=result[1], team_name=result[2])

    def is_player_in_db(self, player_name: str) -> bool:
        self.__api.execute_query(r"select * from {} where name = '{}'".format(self.__table_name, str(player_name).replace("'", "''")))
        if len(self.__api.get_result()) > 0:
            return True
        return False

    def update_player(self, player: Player) -> None:
        self.__api.execute_query(
            "update '{}' set role = '{}', team = '{}' where name = '{}'".format(self.__table_name, player.role,
                                                                                player.team_name.replace("'", "''"), str(player.name).replace("'", "''")))

    def delete_player(self, player_name: str) -> None:
        self.__api.execute_query("DELETE FROM {} WHERE name = '{}'".format(self.__table_name, str(player_name).replace("'", "''")))

    def revert_changes(self):
        self.__api.revert_changes()
