import asyncio

from discord import Message, Member

from command_handlers.ctx import Ctx
from command_handlers.handler import Handler, CommandHandlerException
from commands.update_player import UpdatePlayer
from db_api.storage_framework import StorageFramework, PlayerNotRecognizedException
from team_members.role_enum import RoleEnum


class PlayersAreNotInTheSameTeamException(Exception):
    pass


class DidNotEnterNewCaptainInTime(Exception):
    pass


class CouldNotAssignANewCaptain(Exception):
    pass


class UpdatePlayerCommandHandler(Handler):
    def __init__(self, command: UpdatePlayer, ctx: Ctx):
        super().__init__(command, ctx)
        self.__storage_framework = StorageFramework()

    async def handle(self) -> str:
        try:
            command_author_name = self.ctx.message.author.id
            player_to_update_name = self.command.player.name
            new_captain_representation = ''

            if self.__storage_framework.is_player_in_role(command_author_name, RoleEnum.CAPTAIN):
                if self.__storage_framework.are_players_in_the_same_team(command_author_name, player_to_update_name):
                    if self.__storage_framework.is_player_in_role(player_to_update_name, RoleEnum.CAPTAIN):
                        new_captain = await self.__assign_new_captain(self.ctx.message.author)
                        new_captain_representation = ' and <@{}> to be the new captain'.format(new_captain)
                    self.__storage_framework.update_role_for_player(player_to_update_name, self.command.role)
                    return self.command.get_representation() + new_captain_representation
                else:
                    raise CommandHandlerException('Cannot update players in different teams')
            else:
                raise CommandHandlerException('Only captains are allowed to use this command')
        except PlayerNotRecognizedException:
            raise CommandHandlerException('Only listed player can use this command')
        except CouldNotAssignANewCaptain:
            raise CommandHandlerException('You need to list a new captain within 1 minutes of the "update" command')

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
            self.__storage_framework.update_role_for_player(new_captain_name, RoleEnum.CAPTAIN)
            return new_captain_name
        except DidNotEnterNewCaptainInTime:
            raise CouldNotAssignANewCaptain()
