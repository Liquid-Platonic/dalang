import discord
from discord.sinks import Sink


async def save_recordings(
    sink: Sink, channel: discord.TextChannel, *args
):  # Our voice client already passes these in.
    await channel.send("Processing recording...")
    user_recorded = [  # A list of recorded users
        f"<@{user_id}>" for user_id, audio in sink.audio_data.items()
    ]
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]  # List down the files.
    await channel.send(
        f"Finished recording audio for: {', '.join(user_recorded)}.",
        files=files,
    )  # Send a message with the accumulated files.
