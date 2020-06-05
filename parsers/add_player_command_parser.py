import re

from commands.add_player import AddPlayer
from parsers.bot_command_parser import BotCommandParser, CommandParserException
from model.team_member import TeamMember


class AddPlayerCommandParser(BotCommandParser):
    @classmethod
    def parse(cls, raw_message: str) -> AddPlayer:
        return AddPlayer(TeamMember(cls.__get_id(cls.__get_player_name(raw_message)), '', cls.__get_account(raw_message)))

    @classmethod
    def __get_player_name(cls, message: str) -> str:
        return message.split(' ')[0]

    @staticmethod
    def __get_id(message: str) -> str:
        return re.search(r'\d+', message).group()

    @staticmethod
    def __get_account(message: str) -> str:
        if 'r6stats' not in message:
            raise CommandParserException('Must provide a r6stats link to sign')
        return message.split(' ')[-1]
