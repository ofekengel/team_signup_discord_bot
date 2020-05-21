from commands.update_player import UpdatePlayer
from parsers.bot_command_parser import BotCommandParser


class UpdateCommandParser(BotCommandParser):
    @classmethod
    def parse(cls, raw_message: str) -> UpdatePlayer:
        pass
