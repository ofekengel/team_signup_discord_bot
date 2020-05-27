import asyncio

from discord import Message, Member

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.update_player import UpdatePlayer
from db_api.team_members_db_api import TeamMembersDBAPI
from db_api.teams_db_api import TeamsDBAPI
from team_members.player import Player
from team_members.role_enum import RoleEnum


class PlayerNotRecognizedException(Exception):
    pass


class PlayersAreNotInTheSameTeamException(Exception):
    pass


class DidNotEnterNewCaptainInTime(Exception):
    pass


class CouldNotAssignANewCaptain(Exception):
    pass


class UpdatePlayerCommandHandler(Handler):
    def __init__(self, command: UpdatePlayer, ctx: Ctx):
        super().__init__(command, ctx)
        self.__player_storage_api = TeamMembersDBAPI()
        self.__team_storage_api = TeamsDBAPI()

    async def handle(self) -> str:
        try:
            command_author = self.__get_player_data(self.ctx.message.author.id)
            player_to_update = self.__get_player_data(self.command.player.name)
            new_captain_representation = ''

            if command_author.role == RoleEnum.CAPTAIN.value:
                if self.__are_players_in_the_same_team(command_author.name, player_to_update.name):
                    if player_to_update.role == RoleEnum.CAPTAIN.value:
                        new_captain = await self.__assign_new_captain(self.ctx.message.author)
                        new_captain_representation = ' and <@{}> to be the new captain'.format(new_captain)
                    player_to_update.role = self.command.role.value
                    self.__player_storage_api.update_player(player_to_update)
                    return self.command.get_representation() + new_captain_representation
                else:
                    raise CommandHandlerException('Cannot update players in different teams')
            else:
                raise CommandHandlerException('Only captains are allowed to use this command')
        except PlayerNotRecognizedException:
            raise CommandHandlerException('Only listed player can use this command')
        except CouldNotAssignANewCaptain:
            raise CommandHandlerException('You need to list a new captain within 1 minutes of the "update" command')

    def __get_player_data(self, player_name: str) -> Player:
        if not self.__player_storage_api.is_player_in_db(player_name):
            raise PlayerNotRecognizedException()
        return self.__player_storage_api.get_player(player_name)

    def __are_players_in_the_same_team(self, command_author_name: str, player_to_update_name: str) -> bool:
        if self.__player_storage_api.get_player(command_author_name).team_name == \
                self.__player_storage_api.get_player(player_to_update_name).team_name:
            return True
        return False

    def validate_wanted_message(self, reply_message: Message) -> bool:
        if reply_message.author == self.ctx.message.author and reply_message.channel == self.ctx.message.channel:
            return True
        return False

    async def __get_player_response(self, message_author: Member) -> str:
        self.ctx.bot.awaiting_response.append(message_author)
        try:
            author_response = await self.ctx.bot.wait_for('message', check=self.validate_wanted_message, timeout=10)
        except asyncio.TimeoutError:
            self.ctx.bot.awaiting_response.remove(self.ctx.message.author)
            raise DidNotEnterNewCaptainInTime()
        if len(author_response.raw_mentions) == 1:
            return author_response.raw_mentions[0]
        return await self.__get_player_response(message_author)

    async def __assign_new_captain(self, message_author: Member) -> str:
        try:
            await self.ctx.message.channel.send('{} Please enter a new captain'.format(message_author.mention))
            new_captain_name = await self.__get_player_response(message_author)
            new_captain = self.__get_player_data(new_captain_name)
            new_captain.role = RoleEnum.CAPTAIN.value
            self.__player_storage_api.update_player(new_captain)
            return new_captain_name
        except DidNotEnterNewCaptainInTime:
            raise CouldNotAssignANewCaptain()
