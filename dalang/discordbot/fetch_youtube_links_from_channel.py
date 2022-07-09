import re
from datetime import datetime, timedelta
from typing import List

from discord import TextChannel
from youtube_dl import YoutubeDL

from dalang.discordbot.fetch_messages_from_channel import (
    fetch_all_messages_from_channel,
    fetch_messages_from_channel,
)

links = dict()


async def fetch_youtube_links_from_channel(
    text_channels: List[TextChannel],
    cache_key=None,
    cache_time: int = 5,
    window_minutes: int = 5,
):
    if cache_key and cache_key in links:
        if (
            datetime.now() - timedelta(minutes=cache_time)
            < links[cache_key]["cached_at"]
        ):
            return links[cache_key]
        else:
            links.pop(cache_key)

    yt_pattern = re.compile(
        "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    )
    yt_songs = []
    yt_links = set()
    for text_channel in text_channels:
        channel_messages = await fetch_messages_from_channel(
            text_channel=text_channel, minutes=window_minutes
        )

        for channel_message in channel_messages:
            if not yt_pattern.match(channel_message["message"]):
                continue
            yt_link = yt_pattern.match(channel_message["message"]).string
            if yt_link in yt_links:
                continue
            yt_links.add(yt_link)

    for yt_link in yt_links:
        with YoutubeDL({}) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get("title", None)
            yt_songs.append(
                {
                    "video_url": video_url,
                    "video_id": video_id,
                    "title": video_title,
                }
            )
    links[cache_key] = dict(songs=yt_songs, cached_at=datetime.now())
    return [s["title"] for s in links[cache_key]["songs"]]
