from discord import Message

from commands.icommand import ICommand


class CommandParserException(Exception):
    pass


class BotCommandParser:
    @classmethod
    def parse(cls, message: Message) -> ICommand:
        raise NotImplementedError
