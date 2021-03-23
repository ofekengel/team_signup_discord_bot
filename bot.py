from typing import List, Optional

import discord
from discord import Message, Member, TextChannel

from command_handlers.command_handler_router import CommandHandlerRouter
from command_handlers.ctx import Ctx
from command_handlers.handler import CommandHandlerException
from commands.icommand import ICommand
from config import OFFLINE_MESSAGE, ADMINS, CHANNEL_NAME, TOKEN, ONLINE_MESSAGE, SERVER_NAME
from parsers.bot_command_parser import CommandParserException
from parsers.parser_router import ParserRouter
from utils.temp_discord_message import TempDiscordMessage


class UnknownCommandException(Exception):
    pass


class Bot(discord.Client):
    LOGIN_MESSAGE = '{} online!'
    PATH = __file__[:__file__.rfind('/') + 1]
    MESSAGE_TO_DELETE_FILE = PATH + 'message_to_delete.txt'

    def __init__(self, admins: List[int], channel_name_to_monitor: str, server_name: str, **options):
        super().__init__(**options)
        self.__server_name = server_name
        self.__channel_name_to_monitor = channel_name_to_monitor
        self.__admins = admins
        self.__command_parser_router = ParserRouter
        self.__command_handler_router = CommandHandlerRouter
        self.awaiting_responses: List[Member] = []
        self.__channel_to_monitor: Optional[TextChannel] = None

    async def on_ready(self):
        self.__channel_to_monitor = discord.utils.get(
            discord.utils.get(self.guilds, name=self.__server_name).channels, name=self.__channel_name_to_monitor)
        print(self.LOGIN_MESSAGE.format(self.user.display_name))
        await TempDiscordMessage(self, self.__channel_to_monitor).send(ONLINE_MESSAGE)

    async def on_message(self, message: discord.Message):
        if not message.author.bot and not message.type == discord.MessageType.pins_add:
            if not type(message.channel) == discord.DMChannel:
                if message.channel.name == self.__channel_name_to_monitor and message.author not in self.awaiting_responses:
                    try:
                        parsed_message = self.__parse_message(message.content)
                        result = await self.__handle_message(parsed_message, message)
                        if type(result) == str:
                            await message.channel.send(result)
                        else:
                            await message.channel.send(embed=result)
                    except UnknownCommandException:
                        pass
                        await message.channel.send('Please make sure the first row is:\n sign')
                    except CommandHandlerException as e:
                        print(e.args[0])
                        await message.channel.send(e.args[0])
                    except CommandParserException as e:
                        await message.channel.send(e.args[0])
                        print(e.args[0])
            else:
                if message.author.id in self.__admins and message.content == 'shutdown':
                    await self.__shutdown()
                else:
                    await message.channel.send('dm not supported yet')

    def __parse_message(self, raw_message: str) -> ICommand:
        lines = raw_message.split('\n')
        if len(lines) == 1:
            command = raw_message.split(' ')[0]
        else:
            command = raw_message.split('\n')[0]
        message_with_no_command = self.__trim_command(raw_message)
        try:
            # todo: update all parsers to work with type(Message)
            return self.__command_parser_router[command].parse(message_with_no_command.lower())
        except KeyError:
            raise UnknownCommandException()

    async def __handle_message(self, command: ICommand, message: Message) -> str:
        ctx = Ctx(message.guild, message, self, self.PATH)
        return await self.__command_handler_router[type(command)](ctx).handle(command)

    @staticmethod
    def __trim_command(raw_message):
        command_end_index_in_message = raw_message.find(' ') + 1
        return raw_message[command_end_index_in_message:]

    async def __shutdown(self):
        await TempDiscordMessage(self, self.__channel_to_monitor).send(OFFLINE_MESSAGE)
        await self.logout()


if __name__ == '__main__':
    Bot(ADMINS, CHANNEL_NAME, SERVER_NAME).run(TOKEN)
