import discord
from discord import Message

from command_handlers.command_handler_router import CommandHandlerRouter
from command_handlers.ctx import Ctx
from command_handlers.handler import CommandHandleException
from command_handlers.store_team_command_handler import PlayerAlreadyExistInAnotherRoleException
from commands import icommand
from commands.icommand import ICommand
from parsers.parser_router import ParserRouter
from parsers.sign_command_parser import CouldNotFindTeamNameException, CouldNotFindCaptainNameException


class UnknownCommandException(Exception):
    pass


class Bot(discord.Client):
    LOGIN_MESSAGE = '{} online!'
    BOT_CHANNEL_ID = 711623834507411466

    def __init__(self, **options):
        super().__init__(**options)
        self.__command_parser_router = ParserRouter
        self.__command_handler_router = CommandHandlerRouter

    async def on_ready(self):
        print(self.LOGIN_MESSAGE.format(self.user.display_name))
        # await self.get_channel(self.BOT_CHANNEL_ID).send('online!')

    async def on_message(self, message: discord.Message):
        if message.channel.name == 'bot' and not message.author.bot:
            try:
                parsed_message = self.__parse_message(message.content)
                await message.channel.send(await self.__handle_message(parsed_message, message))
            except UnknownCommandException:
                await message.channel.send('Please use a command. commands are - to be added')
            except CommandHandleException as e:
                await message.channel.send(e.args[0])
            except CouldNotFindTeamNameException:
                await message.channel.send('Please enter team name right')
            except CouldNotFindCaptainNameException:
                await message.channel.send('Please enter captain name right')
            except PlayerAlreadyExistInAnotherRoleException as e:
                await message.channel.send(e.args[0])

    def __parse_message(self, raw_message: str) -> ICommand:
        command = raw_message.split(' ')[0]
        message_with_no_command = self.__trim_command(raw_message)
        try:
            return self.__command_parser_router[command].parse(message_with_no_command)
        except KeyError:
            raise UnknownCommandException()

    async def __handle_message(self, command: icommand, message: Message) -> str:
        # todo: handle multiple guilds
        ctx = Ctx(self.guilds[0], message)
        return await self.__command_handler_router[type(command)](command).handle(ctx)

    @staticmethod
    def __trim_command(raw_message):
        command_end_index_in_message = raw_message.find(' ') + 1
        return raw_message[command_end_index_in_message:]


if __name__ == '__main__':
    Token = 'NzExNjE4MjgyOTA5NzI4ODMw.XsFofw.YgDcC35D8uvKQZINIdeEyZ70IwM'
    Bot().run(Token)
