from commands.icommand import ICommand


class CommandParserException(Exception):
    pass


class BotCommandParser:
    @classmethod
    def parse(cls, raw_message: str) -> ICommand:
        raise NotImplementedError
