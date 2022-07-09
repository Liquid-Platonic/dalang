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
from dalang.discordbot.save_recordings import find_dominant_mood
from dalang.discordbot.youtube_to_genre_mood import get_mood_from_link
from dalang.helpers import get_top_dict_items
from dalang.models import text_to_mood_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
)
from dalang.tagging import TagPredictions
from dalang.types import Emojis


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
    genre: Optional[TagPredictions] = None


@dataclass
class DalangGuild:
    channels: Dict[str, DalangChannel] = field(default_factory=dict)
    mood: Optional[TagPredictions] = None
    genre: Optional[TagPredictions] = None
    param_mood: Optional[str] = None


average = AveragePredictionsAggregator()


class MessageDB:
    messages: Dict[str, DalangGuild] = {}
    links: Dict[str, DalangGuild] = {}
    guild: Guild = None
    user_mood: str = None
    user_genre: str = None

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
            channel = self.links[self.guild.name].channels[
                message.channel.name
            ]
            genre, mood, spotify_id, found = self._calculate_link_mood(
                message.content
            )
            channel.messages.append(DalangMessage(message, genre=genre, mood=mood, found=found))
        else:
            mood = self._calculate_mood(message.content)
            self.messages[self.guild.name].channels[
                message.channel.name
            ].messages.append(DalangMessage(message, mood=mood))

        self.update_channel(message.channel)
        self.update_guild()

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
                channel.mood = self._calculate_channel_mood(channel.messages)

        guild.mood = self._calculate_guild_mood(guild.channels.values())
        return guild.mood

    def calculate_link_mood(self):
        guild = self.links[self.guild.name]
        for channel_name, channel in self.links[
            self.guild.name
        ].channels.items():
            did_message_changed = False
            for message in channel.messages:
                if (
                    not message.mood or not message.genre
                ) and not message.found:
                    genre, mood, spotify_id, found = self._calculate_link_mood(
                        message.message.content
                    )
                    message.mood = mood
                    message.genre = genre
                    message.found = found
                    did_message_changed = True

            if did_message_changed or not channel.mood:
                channel.mood = self._calculate_channel_mood(channel.messages)
                channel.genre = self._calculate_channel_genre(channel.messages)

        guild.mood = self._calculate_guild_mood(guild.channels.values())
        guild.genre = self._calculate_guild_genre(guild.channels.values())
        return guild.mood

    @staticmethod
    def _calculate_channel_mood(messages):
        return (
            average.aggregate_linear(reversed([m.mood for m in messages if m.mood]))
            if messages
            else None
        )

    @staticmethod
    def _calculate_channel_genre(messages):
        return (
            average.aggregate_linear(reversed([m.genre for m in messages if m.genre]))
            if messages
            else None
        )

    @staticmethod
    def _calculate_guild_mood(channels):
        return (
            average.aggregate([c.mood for c in channels if c.mood])
            if channels
            else None
        )

    @staticmethod
    def _calculate_guild_genre(channels):
        return (
            average.aggregate([c.genre for c in channels if c.genre])
            if channels
            else None
        )

    @staticmethod
    def _calculate_mood(message: str):
        return text_to_mood_model.predict(message[:512])

    @staticmethod
    def _calculate_link_mood(link):
        genre, mood, spotify_ids, found = get_mood_from_link(link)
        if not found:
            return None, None, None, False
        return genre, mood, spotify_ids, True

    def update_guild(self):
        guild = self.messages[self.guild.name]
        guild.mood = self._calculate_guild_mood(guild.channels.values())
        link_guild = self.links[self.guild.name]
        link_guild.mood = self._calculate_guild_mood(
            link_guild.channels.values()
        )

    def update_channel(self, channel: TextChannel):
        db_channel = self.get_channel(channel.name)
        new_mood = self._calculate_channel_mood(db_channel.messages)
        new_genre = self._calculate_channel_genre(db_channel.messages)
        if self._did_change(new_mood, db_channel.mood) or self._did_change(new_genre, db_channel.genre):
            asyncio.create_task(
                self.on_channel_update(
                    channel,
                    new_mood,
                    new_genre,
                    db_channel.mood,
                    db_channel.genre,
                )
            )
        db_channel.genre = new_genre
        db_channel.mood = new_mood

    def get_channel(self, name):
        return self.messages[self.guild.name].channels[name]

    async def on_channel_update(
        self,
        channel: TextChannel,
        c_mood,
        c_genre,
        p_mood,
        p_genre,
        isLink: bool,
    ):
        dm = find_dominant_mood(c_mood) or {}
        dominant_mood = dm.get("mood", None)
        pm = find_dominant_mood(p_mood) or {}
        p_dominant_mood = pm.get("mood", None)
        if channel and dominant_mood != p_dominant_mood and not isLink:
            # await channel.send(
            #     f"Channel `{channel.name}` mood was changed from {p_dominant_mood} to {dominant_mood}"
            # )
            if Emojis[dominant_mood]:
                name = channel.name
                for feeling in Emojis:
                    name = name.replace(feeling, '')
                await channel.edit(name=f"{Emojis[dominant_mood]}-{name}")
            return
        else:
            return

    def set_mood(self, mood):
        self.user_mood = mood

    def set_genre(self, genre):
        self.user_genre = genre

    def _did_change(self, new_genre, genre) -> bool:
        if find_dominant_mood(new_genre) != find_dominant_mood(genre):
            return True
        return False

dbs = {}


def message_db(guild: Guild) -> MessageDB:
    if guild.name in dbs:
        return dbs[guild.name]

    guild_db = MessageDB(guild)
    guild_db.setup()
    dbs[guild.name] = guild_db
    return guild_db
