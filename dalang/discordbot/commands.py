import asyncio
import re
from collections import defaultdict
from typing import List, Optional

from discord.sinks import MP3Sink, WaveSink

from dalang.apis.cyaniteapi import CyaniteApi
from dalang.crawling import SpotifyIDCrawler
from dalang.discordbot.client import bot, find_voice_client
from dalang.discordbot.fetch_messages_from_channel import (
    fetch_messages_from_channel,
)
from dalang.discordbot.fetch_youtube_links_from_channel import (
    fetch_youtube_links_from_channel,
)
from dalang.discordbot.helpers import batch_string
from dalang.discordbot.mood_collector import mood_collector
from dalang.discordbot.prepare_channel_messages_for_text_to_mood import (
    prepare_channel_messages_for_text_to_mood,
)
from dalang.discordbot.save_recordings import (
    find_mood_from_recordings,
    save_recordings,
)
from dalang.discordbot.views import MoodSelectView
from dalang.discordbot.youtube_to_genre_mood import youtube_to_genre_mood
from dalang.helpers import get_top_dict_items, merge_dicts
from dalang.models import cyanite_model, text_to_mood_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
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
    if not voice_client or not voice_client.is_connected():
        await ctx.invoke(bot.get_command("killme"))
        await ctx.invoke(bot.get_command("dalang"))
        voice_client = find_voice_client(ctx.guild)
    if not voice_client.is_connected():
        await ctx.send("Bot is not connected to voice channel")
        return

    voice_client.start_recording(
        WaveSink(),  # The sink type to use.
        find_mood_from_recordings,  # What to do once done.
        ctx.channel,  # The channel to disconnect from.
        ctx.guild.name,
        False,
    )
    await ctx.send(f"Start Monitoring")

    for index in range(100):
        await asyncio.sleep(10)
        if voice_client.recording:
            voice_client.stop_recording()

        await asyncio.sleep(5)
        if not voice_client.recording:
            voice_client.start_recording(
                WaveSink(),  # The sink type to use.
                find_mood_from_recordings,  # What to do once done.
                ctx.channel,  # The channel to disconnect from.
                ctx.guild.name,
                False,
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
    return
    text_channels = ctx.guild.text_channels
    songs = await fetch_youtube_links_from_channel(
        text_channels, ctx.guild.name
    )
    print(songs)


@bot.command()
async def youtube_to_cyanite_tags(
    ctx,
    text_channel: Optional[str] = None,
    window_minutes: Optional[int] = None,
):
    return
    text_channels = ctx.guild.text_channels
    if text_channel:
        text_channels = [tc for tc in text_channels if tc.name == text_channel]

    genres, moods, spotify_ids = await youtube_to_genre_mood(
        text_channels, window_minutes
    )
    await ctx.send(spotify_ids)
    await ctx.send({"genres": genres, "moods": moods})
    return genres, moods


@bot.command()
async def recommend(ctx, num_of_songs=2):
    guild = ctx.guild.name
    speech_moods = mood_collector.get(guild)
    if not speech_moods:
        await ctx.send("Need to monitor before recommending")
        return

    voice_client = find_voice_client(ctx.guild)
    if voice_client:
        voice_client.stop_recording()

    text_channels = ctx.guild.text_channels
    (
        links_genre_predictions,
        links_mood_predictions,
        _,
    ) = await youtube_to_genre_mood(text_channels, 10)

    model_inputs = await prepare_channel_messages_for_text_to_mood(ctx, [])
    text_predictions = text_to_mood_model.predict_batch(
        batch_string(model_inputs, 512)
    )

    last_speech_mood = speech_moods[0]
    average_aggregator = AveragePredictionsAggregator()
    average_mood = average_aggregator.aggregate(
        [mood_vector for user, mood_vector in last_speech_mood.items()]
    )
    average_mood_with_text_and_links = average_aggregator.aggregate(
        [average_mood, *text_predictions, links_mood_predictions or {}]
    )
    keywords = merge_dicts(
        [
            get_top_dict_items(average_mood_with_text_and_links, 4),
            get_top_dict_items(links_genre_predictions, 3),
        ]
    )
    spotify_ids = CyaniteApi().get_spotify_ids_by_keywords(keywords)

    await ctx.channel.send("Sending keywords")
    await ctx.channel.send(str(keywords))

    # print track links
    if spotify_ids:
        for index in range(min(num_of_songs, 10)):
            track = SpotifyIDCrawler().get_track_by_id(spotify_ids[index])
            if track["external_urls"]:
                await ctx.channel.send(
                    f"{list(track['external_urls'].values())[0]}"
                )
    else:
        await ctx.channel.send("No spotify ids found")


# try select box - but is not working
@bot.command()
async def flavor(ctx):
    await ctx.send("Choose a flavor!", view=MoodSelectView())
