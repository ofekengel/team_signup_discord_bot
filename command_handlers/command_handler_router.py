from typing import MutableMapping, Type

from command_handlers.add_player_command_handler import AddPlayerCommandHandler
from command_handlers.delete_command_handler import DeleteCommandHandler
from command_handlers.handler import Handler
from command_handlers.store_team_command_handler import StoreTeamCommandHandler
from command_handlers.update_player_command_handler import UpdatePlayerCommandHandler
from commands.add_player import AddPlayer
from commands.delete_player import DeletePlayer
from commands.icommand import ICommand
from commands.store_team import StoreTeam
from commands.update_player import UpdatePlayer

CommandHandlerRouter: MutableMapping[Type[ICommand], Type[Handler]] = {StoreTeam: StoreTeamCommandHandler,
                                                                       UpdatePlayer: UpdatePlayerCommandHandler,
                                                                       DeletePlayer: DeleteCommandHandler,
                                                                       AddPlayer: AddPlayerCommandHandler}
