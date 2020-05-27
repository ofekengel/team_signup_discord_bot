import re

from commands.update_player import UpdatePlayer
from parsers.bot_command_parser import BotCommandParser
from team_members.player import Player
from team_members.role_enum import RoleEnum


class RoleDoesNotExistException(Exception):
    pass


class UpdateCommandParser(BotCommandParser):
    @classmethod
    def parse(cls, message: str) -> UpdatePlayer:
        player_name = cls.__get_id(cls.__get_player_name(message))
        role = cls.__get_player_role(message)
        if role not in RoleEnum._value2member_map_:
            raise RoleDoesNotExistException()
        return UpdatePlayer(Player(player_name, ''), RoleEnum._value2member_map_[role])

    @classmethod
    def __get_player_name(cls, message: str) -> str:
        return message.split(' ')[0]

    @classmethod
    def __get_player_role(cls, message: str) -> str:
        return message[re.search('to role', message).regs[0][1] + 1:]

    @staticmethod
    def __get_id(message: str) -> str:
        return re.search(r'\d+', message).group()
