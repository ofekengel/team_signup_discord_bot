from typing import NamedTuple

from discord import Guild, Message, Client


class Ctx(NamedTuple):
    server: Guild
    message: Message
    bot: Client
    path: str
