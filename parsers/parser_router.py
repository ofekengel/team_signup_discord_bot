from typing import MutableMapping, Type

from commands.bot_commands_enum import BotCommands
from parsers.add_player_command_parser import AddPlayerCommandParser
from parsers.bot_command_parser import BotCommandParser
from parsers.delete_command_parser import DeleteCommandParser
from parsers.sign_command_parser import SignCommandParser
from parsers.update_command_parser import UpdateCommandParser

ParserRouter: MutableMapping[str, Type[BotCommandParser]] = {BotCommands.SIGN.value: SignCommandParser,
                                                             BotCommands.UPDATE.value: UpdateCommandParser,
                                                             BotCommands.DELETE.value: DeleteCommandParser,
                                                             BotCommands.ADD.value: AddPlayerCommandParser}
