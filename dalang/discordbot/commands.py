import re
from typing import List
import asyncio

import discord
from discord.sinks import MP3Sink, WaveSink

from dalang.discordbot.client import bot, find_voice_client
from dalang.discordbot.fetch_messages_from_channel import (
    fetch_messages_from_channel,
)
from dalang.discordbot.fetch_youtube_links_from_channel import (
    fetch_youtube_links_from_channel,
)
from dalang.discordbot.prepare_channel_messages_for_text_to_mood import (
    prepare_channel_messages_for_text_to_mood,
)
from dalang.discordbot.save_recordings import save_recordings
from dalang.models import text_to_mood_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
from dalang.discordbot.save_recordings import (
    find_mood_from_recordings,
    save_recordings,
)


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
async def monitor(ctx):
    voice_client = find_voice_client(ctx.guild)
    if not voice_client:
        await ctx.invoke(bot.get_command("dalang"))
        voice_client = find_voice_client(ctx.guild)
    voice_client.start_recording(
        WaveSink(),  # The sink type to use.
        find_mood_from_recordings,  # What to do once done.
        ctx.channel,  # The channel to disconnect from.
    )
    await asyncio.sleep(5)

    await ctx.send(f"Start Monitoring")

    for index in range(100):
        await asyncio.sleep(5)
        if voice_client.recording:
            await ctx.send(":stop_sign: Stopping record!")
            voice_client.stop_recording()

            await asyncio.sleep(10)
            voice_client.play(
                discord.FFmpegPCMAudio(f"temp/file{ctx.author.id}.wav")
            )

        await asyncio.sleep(5)
        if not voice_client.recording:
            await ctx.send(":studio_microphone: Starting record!")
            voice_client.start_recording(
                WaveSink(),  # The sink type to use.
                find_mood_from_recordings,  # What to do once done.
                ctx.channel,  # The channel to disconnect from.
            )

    if voice_client.recording:
        await ctx.send(":stop_sign: Stopping record!")
        voice_client.stop_recording()

    await ctx.send("Finished Monitoring")


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
async def messages_to_mood(ctx, *channel_names):
    # channel_names = *channel_names
    model_inputs = await prepare_channel_messages_for_text_to_mood(
        ctx, channel_names
    )
    prediction = text_to_mood_model.predict(model_inputs)
    # predictions = text_to_mood_model.predict_batch(model_inputs)
    # prediction = AveragePredictionsAggregator.aggregate(predictions)
    await ctx.send(f"Prediction: {prediction}")


@bot.command()
async def youtube_songs(ctx):
    text_channels = ctx.guild.text_channels
    songs = await fetch_youtube_links_from_channel(
        text_channels, ctx.guild.name
    )
    print(songs)
    return songs


@bot.command()
async def song_mood(ctx):
    songs = await ctx.invoke(bot.get_command("youtube_songs"))

    print(songs)
