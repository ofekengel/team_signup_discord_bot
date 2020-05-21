from commands.icommand import ICommand


class BotCommandParser:
    @classmethod
    def parse(cls, raw_message: str) -> ICommand:
        raise NotImplementedError
