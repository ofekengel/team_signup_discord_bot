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


OFFLINE_MESSAGE = """Dear Teams,

The sign-up bot is offline right now. 
The bot is online every day from 16:00 CET till 23:00 CET. Please try it again tomorrow!

Thanks for your patience, 
The technic team"""


class Bot(discord.Client):
    LOGIN_MESSAGE = '{} online!'

    def __init__(self, **options):
        super().__init__(**options)
        self.__command_parser_router = ParserRouter
        self.__command_handler_router = CommandHandlerRouter
        self.awaiting_response: List[Member] = []
        self.BOT_CHANNEL_ID = 0

    async def on_ready(self):
        self.BOT_CHANNEL_ID = discord.utils.get(discord.utils.get(self.guilds, name='pt').channels, name='bot').id
        print(self.LOGIN_MESSAGE.format(self.user.display_name))
        await self.__delete_last_bot_status_message()
        await self.__send_bot_status_message('online!')

    async def on_message(self, message: discord.Message):
        if not message.author.bot and not message.type == discord.MessageType.pins_add:
            if not type(message.channel) == discord.DMChannel:
                if message.channel.name == 'bot' and not message.author.bot and message.author not in self.awaiting_response:
                    try:
                        parsed_message = self.__parse_message(message.content)
                        result = await self.__handle_message(parsed_message, message)
                        if type(result) == str:
                            await message.channel.send(result)
                        else:
                            await message.channel.send(embed=result)
                    except UnknownCommandException:
                        await message.channel.send('Please use a command. commands are - to be added')
                    except CommandHandlerException as e:
                        await message.channel.send(e.args[0])
                    except CommandParserException as e:
                        await message.channel.send(e.args[0])
            else:
                if message.author.id == 158297103276310528 and message.content == 'shutdown':
                    await self.__delete_last_bot_status_message()
                    await self.__send_bot_status_message(OFFLINE_MESSAGE)
                    await self.logout()
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
            # todo: update all parsers to work with Message
            return self.__command_parser_router[command].parse(message_with_no_command.lower())
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

    async def __delete_last_bot_status_message(self) -> None:
        with open('message_to_delete.txt', 'r') as f:
            message_to_delete_id = f.read()
        await self.http.delete_message(self.BOT_CHANNEL_ID, message_to_delete_id)

    async def __send_bot_status_message(self, message: str) -> None:
        shutdown_message = await self.get_channel(self.BOT_CHANNEL_ID).send(
            message)
        with open('message_to_delete.txt', 'w') as f:
            f.write(str(shutdown_message.id))


if __name__ == '__main__':
    Token = 'NzE2MzIxNDkyNjM5Njc4NDY0.XtKEcQ.dhbnJ6RCOoV85QUyTUSdBIuvxXU'
    Bot().run(Token)
