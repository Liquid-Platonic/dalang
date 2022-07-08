import re

from discord.sinks import MP3Sink
from youtube_dl import YoutubeDL

from dalang.discordbot.client import bot, find_voice_client
from dalang.discordbot.fetch_messages_from_channel import (
    fetch_messages_from_channel,
)
from dalang.discordbot.save_recordings import save_recordings


@bot.command(name="dalang")
async def dalang(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.channel.send(f"You are not in a voice channel")


@bot.command()
async def killme(ctx):
    voice_client = find_voice_client(ctx.guild)
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.channel.send(f"Bot is not in a voice channel")


@bot.command()
async def record(ctx):
    voice_client = find_voice_client(ctx.guild)
    if not voice_client:
        return await ctx.channel.send(f"Bot is not in a voice channel")

    voice_client.start_recording(
        MP3Sink(),  # The sink type to use.
        save_recordings,  # What to do once done.
        ctx.channel,  # The channel to disconnect from.
    )

    await ctx.send(f"Start Recording")


@bot.command()
async def stop(ctx):
    voice_client = find_voice_client(ctx.guild)
    if not voice_client or not voice_client.recording:
        return await ctx.channel.send(
            f"Bot is not in a voice channel or is not recording!"
        )

    if voice_client.recording:
        voice_client.stop_recording()


@bot.command()
async def messages(ctx):
    text_channels = ctx.guild.text_channels
    channel_messages = {}
    for text_channel in text_channels:
        channel_name = text_channel.name
        msgs = await fetch_messages_from_channel(
            text_channel=text_channel, minutes=5
        )
        channel_messages[channel_name] = msgs

    """
    messages object is like that!
    {
        "channel_name_1": [{author, message, time}],
        "channel_name_2": [{author, message, time}],
        "channel_name_2": [{author, message, time}],
    }
    """
    return channel_messages


@bot.command()
async def youtube_songs(ctx):
    yt_pattern = re.compile(
        "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    )
    text_channels = ctx.guild.text_channels
    yt_songs = []

    for text_channel in text_channels:
        channel_messages = await fetch_messages_from_channel(
            text_channel=text_channel
        )
        for channel_message in channel_messages:
            if yt_pattern.match(channel_message["message"]):
                with YoutubeDL({}) as ydl:
                    info_dict = ydl.extract_info(
                        channel_message["message"], download=False
                    )
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

    print(yt_songs)