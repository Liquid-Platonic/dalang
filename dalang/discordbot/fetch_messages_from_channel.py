from datetime import datetime, timedelta

from .client import bot

guild_messages = dict()


async def fetch_all_messages_from_channel(
    text_channel, cache_key: str = None, cache_time: int = 5
):
    if cache_key and cache_key in guild_messages:
        if (
            datetime.now() - timedelta(minutes=cache_time)
            < guild_messages[cache_key]["cached_at"]
        ):
            return guild_messages[cache_key]
        else:
            guild_messages.pop(cache_key)

    messages = await fetch_messages_from_channel(text_channel)

    guild_messages[cache_key] = dict(
        messages=messages, cached_at=datetime.now()
    )
    return guild_messages[cache_key]["messages"]


async def fetch_messages_from_channel(text_channel, minutes=None):
    channel_messages = []

    # take messages_history x minutes before until now in utc or take messages_history of all time
    messages_history = (
        text_channel.history(
            limit=None,
            after=datetime.now() - timedelta(minutes=minutes),
        )
        if minutes
        else text_channel.history(limit=None)
    )

    async for message in messages_history:
        if not message.author == bot.user:
            message_details = {
                "author": message.author,
                "message": message.content,
                "time": message.created_at,
            }
            channel_messages.append(message_details)

    return channel_messages
