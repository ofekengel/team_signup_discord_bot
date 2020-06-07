import re

from commands.delete_player import DeletePlayer
from parsers.bot_command_parser import BotCommandParser
from model.player import Player


class DeleteCommandParser(BotCommandParser):
    @classmethod
    def parse(cls, raw_message: str) -> DeletePlayer:
        return DeletePlayer(Player(cls.__get_id(cls.__get_player_name(raw_message)), ''))

    @classmethod
    def __get_player_name(cls, message: str) -> str:
        return message.split(' ')[0]

    @staticmethod
    def __get_id(message: str) -> str:
        return re.search(r'\d+', message).group()
