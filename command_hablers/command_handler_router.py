from typing import MutableMapping, Type

from command_hablers.handler import Handler
from command_hablers.store_team_command_handler import StoreTeamCommandHandler
from commands.icommand import ICommand
from commands.store_team import StoreTeam
from commands.update_player import UpdatePlayer

CommandHandlerRouter: MutableMapping[Type[ICommand], Type[Handler]] = {StoreTeam: StoreTeamCommandHandler,
                                                                       UpdatePlayer: None}
