from datetime import datetime, timedelta

from .client import bot


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
