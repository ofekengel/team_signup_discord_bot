from typing import NamedTuple

from discord import Guild, Message


class Ctx(NamedTuple):
    server: Guild
    message: Message
