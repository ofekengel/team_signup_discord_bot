from typing import MutableMapping, Type

from commands.bot_commands_enum import BotCommands
from parsers.bot_command_parser import BotCommandParser
from parsers.sign_command_parser import SignCommandParser

ParserRouter: MutableMapping[str, Type[BotCommandParser]] = {BotCommands.SIGN.value: SignCommandParser}
