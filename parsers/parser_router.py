from typing import MutableMapping, Type

from commands.bot_commands_enum import BotCommands
from parsers.bot_command_parser import BotCommandParser
from parsers.sign_command_parser import SignCommandParser
from parsers.update_command_parser import UpdateCommandParser

ParserRouter: MutableMapping[str, Type[BotCommandParser]] = {BotCommands.SIGN.value: SignCommandParser,
                                                             BotCommands.UPDATE.value: UpdateCommandParser}
