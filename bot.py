from typing import List

import discord
from discord import Message, Member

from command_handlers.command_handler_router import CommandHandlerRouter
from command_handlers.ctx import Ctx
from command_handlers.handler import CommandHandlerException
from commands.icommand import ICommand
from parsers.bot_command_parser import CommandParserException
from parsers.parser_router import ParserRouter


class UnknownCommandException(Exception):
    pass


class Bot(discord.Client):
    LOGIN_MESSAGE = '{} online!'
    BOT_CHANNEL_ID = 711623834507411466

    def __init__(self, **options):
        super().__init__(**options)
        self.__command_parser_router = ParserRouter
        self.__command_handler_router = CommandHandlerRouter
        self.awaiting_response: List[Member] = []

    async def on_ready(self):
        print(self.LOGIN_MESSAGE.format(self.user.display_name))
        await self.get_channel(self.BOT_CHANNEL_ID).send('online!')

    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            if not type(message.channel) == discord.DMChannel:
                if message.channel.name == 'bot' and not message.author.bot and message.author not in self.awaiting_response:
                    try:
                        parsed_message = self.__parse_message(message.content)
                        result = await self.__handle_message(parsed_message, message)
                        await message.channel.send(result)
                    except UnknownCommandException:
                        await message.channel.send('Please use a command. commands are - to be added')
                    except CommandHandlerException as e:
                        await message.channel.send(e.args[0])
                    except CommandParserException as e:
                        await message.channel.send(e.args[0])
            else:
                await message.channel.send('dm not supported yet')

    def __parse_message(self, raw_message: str) -> ICommand:
        command = raw_message.split(' ')[0]
        message_with_no_command = self.__trim_command(raw_message)
        try:
            # todo: update all parsers to work with Message
            return self.__command_parser_router[command].parse(message_with_no_command)
        except KeyError:
            raise UnknownCommandException()

    async def __handle_message(self, command: ICommand, message: Message) -> str:
        # todo: handle multiple guilds
        ctx = Ctx(self.guilds[0], message, self)
        return await self.__command_handler_router[type(command)](command, ctx).handle()

    @staticmethod
    def __trim_command(raw_message):
        command_end_index_in_message = raw_message.find(' ') + 1
        return raw_message[command_end_index_in_message:]


if __name__ == '__main__':
    Token = 'NzExNjE4MjgyOTA5NzI4ODMw.XsFofw.YgDcC35D8uvKQZINIdeEyZ70IwM'
    Bot().run(Token)
