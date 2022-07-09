import asyncio
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Dict, List, Optional, Tuple

from discord import Guild, Message, TextChannel

from dalang.discordbot.fetch_messages_from_channel import (
    fetch_all_messages_from_channel,
)
from dalang.discordbot.fetch_youtube_links_from_channel import (
    fetch_title_from_link,
)
from dalang.discordbot.youtube_to_genre_mood import get_mood_from_link
from dalang.models import text_to_mood_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
)
from dalang.tagging import TagPredictions


@dataclass
class DalangMessage:
    message: Message
    genre: Optional[TagPredictions] = None
    mood: Optional[TagPredictions] = None
    found: bool = False


@dataclass
class DalangChannel:
    messages: List[DalangMessage] = field(default_factory=list)
    mood: Optional[TagPredictions] = None


@dataclass
class DalangGuild:
    channels: Dict[str, DalangChannel] = field(default_factory=dict)
    mood: Optional[TagPredictions] = None
    param_mood: Optional[str] = None


average = AveragePredictionsAggregator()


class MessageDB:
    messages: Dict[str, DalangGuild] = {}
    links: Dict[str, DalangGuild] = {}
    guild: Guild = None

    def __init__(self, guild: Guild):
        self.guild = guild
        if not guild.name:
            raise ValueError("You must pass guild_name")

        self.messages[guild.name] = DalangGuild()
        self.links[guild.name] = DalangGuild()

    def setup(self):
        asyncio.create_task(self.init_guild_storage())

    @property
    def yt_pattern(self):
        return re.compile(
            "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
        )

    def _is_str_yt_link(self, input_str: str) -> bool:
        return self.yt_pattern.match(input_str)

    async def _fill_channel_data(
        self, channel: TextChannel
    ) -> Tuple[List[DalangMessage], List[DalangMessage]]:
        channel_links = []
        channel_messages = []
        for message in await fetch_all_messages_from_channel(channel):
            if self._is_str_yt_link(message.content):
                channel_links.append(DalangMessage(message))
            else:
                channel_messages.append(DalangMessage(message))
        return channel_messages, channel_links

    async def init_guild_storage(self) -> None:
        for channel in self.guild.channels:
            if isinstance(channel, TextChannel):
                (
                    channel_messages,
                    channel_links,
                ) = await self._fill_channel_data(channel)

                if channel.name not in self.messages[self.guild.name].channels:
                    self.messages[self.guild.name].channels[
                        channel.name
                    ] = DalangChannel()
                if channel.name not in self.links[self.guild.name].channels:
                    self.links[self.guild.name].channels[
                        channel.name
                    ] = DalangChannel()
                self.messages[self.guild.name].channels[
                    channel.name
                ].messages.extend(channel_messages)
                self.links[self.guild.name].channels[
                    channel.name
                ].messages.extend(channel_links)

        self.calculate_mood()
        self.calculate_link_mood()

    def add(self, message: Message):
        if message.channel.name not in self.messages[self.guild.name].channels:
            self.messages[self.guild.name].channels[
                message.channel.name
            ] = DalangChannel()
        if message.channel.name not in self.links[self.guild.name].channels:
            self.links[self.guild.name].channels[
                message.channel.name
            ] = DalangChannel()

        if self._is_str_yt_link(message.content):
            self.links[self.guild.name].channels[
                message.channel.name
            ].messages.append(DalangMessage(message))
        else:
            self.messages[self.guild.name].channels[
                message.channel.name
            ].messages.append(DalangMessage(message))

    def calculate_mood(self):
        guild = self.messages[self.guild.name]
        for channel_name, channel in self.messages[
            self.guild.name
        ].channels.items():
            did_message_changed = False
            for message in channel.messages:
                if not message.mood:
                    message.mood = self._calculate_mood(
                        message.message.content
                    )
                    did_message_changed = True

            if did_message_changed or not channel.mood:
                channel.mood = average.aggregate(
                    [m.mood for m in channel.messages if m.mood]
                )

        guild.mood = average.aggregate(
            [c.mood for c in guild.channels.values() if c.mood]
        )
        return guild.mood

    def calculate_link_mood(self):
        guild = self.links[self.guild.name]
        for channel_name, channel in self.links[
            self.guild.name
        ].channels.items():
            did_message_changed = False
            for message in channel.messages:
                if not (message.mood or not message.genre) and message.found:
                    genre, mood, spotify_id, found = self._calculate_link_mood(
                        message.message.content
                    )
                    message.mood = mood
                    message.genre = genre
                    message.found = found
                    did_message_changed = True

            if did_message_changed or not channel.mood:
                channel.mood = average.aggregate(
                    [m.mood for m in channel.messages if m.mood]
                )

        guild.mood = average.aggregate(
            [c.mood for c in guild.channels.values() if c.mood]
        )
        return guild.mood

    @staticmethod
    def _calculate_mood(message: str):
        return text_to_mood_model.predict(message[:512])

    @staticmethod
    def _calculate_link_mood(link):
        genre, mood, spotify_ids, found = get_mood_from_link(link)
        if not found:
            return None, None, None, False
        return genre, mood, spotify_ids, True


dbs = {}


def message_db(guild: Guild) -> MessageDB:
    if guild.name in dbs:
        return dbs[guild.name]

    guild_db = MessageDB(guild)
    guild_db.setup()
    dbs[guild.name] = guild_db
    return guild_db
