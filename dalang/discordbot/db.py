import re
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Any, Dict, List, Optional, Tuple

from discord import Guild, Message, TextChannel

from dalang.discordbot.fetch_messages_from_channel import (
    fetch_all_messages_from_channel,
)
from dalang.tagging import TagPredictions


@dataclass
class DalangMessage:
    message: Message
    mood: Optional[TagPredictions]


@dataclass
class DalangChannel:
    messages: List[DalangMessage]
    mood: Optional[TagPredictions] = None


@dataclass
class DalangGuild:
    channels: Dict[str, DalangChannel] = {}
    mood: Optional[TagPredictions] = None


class MessageDB:

    guild_messages: DalangGuild
    guild_links: DalangGuild
    guild = None

    def __init__(self, guild: Guild):
        self.guild = guild
        if not guild.name:
            raise ValueError("You must pass guild_name")

        self.init_guild_storage()

    @property
    def yt_pattern(self):
        return re.compile(
            "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
        )

    def _is_str_yt_link(self, input_str: str) -> bool:
        return self.yt_pattern.match(input_str)

    async def _fill_channel_data(
        self, channel: TextChannel
    ) -> Tuple[DalangChannel, DalangChannel]:
        channel_links = []
        channel_messages = []
        async for message in fetch_all_messages_from_channel(channel):
            if self._is_str_yt_link(message.content):
                channel_links.append(DalangMessage(message))
            else:
                channel_messages.append(DalangMessage(message))
        message_channel = DalangChannel(messages=channel_messages)
        links_channel = DalangChannel(messages=channel_links)
        return message_channel, links_channel

    async def init_guild_storage(self) -> None:
        messages_channels = {}
        links_channels = {}
        for channel in self.guild.channels:
            channel_messages, channel_links = self._fill_channel_data(channel)
            messages_channels[channel.name] = channel_messages
            links_channels[channel.name] = channel_links
        self.guild_messages = DalangGuild(channels=messages_channels)
        self.guild_links = DalangGuild(channels=links_channels)

    def add(self, message: Message):
        if self._is_str_yt_link(message.content):

            self.guild_links.channels[message.channel.name].messages.append(
                (DalangMessage(message))
            )
        else:
            self.guild_messages.channels[message.channel.name].messages.append(
                (DalangMessage(message))
            )


dbs = {}


def message_db(guild: Guild) -> MessageDB:
    if guild.name in dbs:
        return dbs[guild.name]

    guild_db = MessageDB(guild)
    dbs[guild.name] = guild_db
    return guild_db
