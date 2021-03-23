from pathlib import Path

import discord
from discord import TextChannel


class NoLastMessageException(Exception):
    pass


class TempDiscordMessage(object):
    __folder__ = Path(__file__).parent

    def __init__(self, client: discord.Client, channel: TextChannel):
        self.channel = channel
        self.client = client

    @property
    def __last_message_id(self) -> int:
        try:
            with open(self.__folder__ + self.channel.id, 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            raise NoLastMessageException()

    @__last_message_id.setter
    def __last_message_id(self, id: int) -> None:
        with open(self.__folder__ + self.channel.id, 'w') as f:
            f.write(str(id))

    async def send(self, message: str):
        try:
            self.client.http.delete_message(self.channel.id, self.__last_message_id)
        except (discord.errors.NotFound, NoLastMessageException):
            pass
        sent_message = await self.channel.send(message)
        self.__last_message_id = sent_message.id
