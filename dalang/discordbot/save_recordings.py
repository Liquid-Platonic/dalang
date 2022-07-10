import wave
from pathlib import Path

import discord
from discord.sinks import Sink

from dalang.discordbot.mood_collector import mood_collector
from dalang.discordbot.views import ButtonView
from dalang.models import speech_to_mood_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
)


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


def find_dominant_mood(prediction):
    if not prediction:
        return None
    feeling = max(
        [{"mood": key, "value": value} for key, value in prediction.items()],
        key=lambda x: x["value"],
    )
    return feeling


async def find_mood_from_recordings(
    sink: Sink,
    channel: discord.TextChannel,
    guild_name,
    write_output=True,
    *args,
):  # Our voice client already passes these in.
    if write_output:
        await channel.send("Processing recordings' mood...")

    user_recorded = [  # A list of recorded users
        f"<@{user_id}>" for user_id, audio in sink.audio_data.items()
    ]

    filepaths = []
    for index, audio in sink.audio_data.items():
        filename = f"temp/file{index}.wav"

        with wave.open(filename, "wb") as wav:
            # wav.setparams((1, 16, 44100, 0, 'NONE', 'not compressed'))
            wav.setnchannels(1)  # mono
            wav.setsampwidth(2)
            wav.setframerate(96000)
            # wav.setnchannels(1)
            wav.writeframesraw(audio.file.read())

        filepaths.append(filename)

    predictions = [
        speech_to_mood_model.predict(Path(file).absolute())
        for file in filepaths
    ]

    payload = {
        user_id: predictions[index]
        for index, (user_id, _) in enumerate(sink.audio_data.items())
    }

    avg_aggregator = AveragePredictionsAggregator()
    average_mood = (
        avg_aggregator.aggregate(predictions) if predictions else None
    )
    new_dominant_mood = (
        find_dominant_mood(average_mood) if average_mood else {}
    )
    speech_moods = mood_collector.get(guild_name)
    old_dominant_mood = {}
    if speech_moods:
        old_average_mood = avg_aggregator.aggregate(
            [mood_vector for user, mood_vector in speech_moods[0].items()]
        )
        old_dominant_mood = find_dominant_mood(old_average_mood)
    old_mood = old_dominant_mood.get("mood", None)
    new_mood = new_dominant_mood.get("mood", None)
    if old_mood != new_mood:
        if not old_mood:
            message = f"Voice Channel Mood detected as: `{new_mood}`!"
        else:
            message = f"Voice Channel Mood changed from: `{old_mood}` to: `{new_mood}`!"
        await channel.send(message)

        mood_collector.add(payload, guild_name)

    if write_output:
        for index, prediction in enumerate(predictions):
            feeling = find_dominant_mood(prediction)
            await channel.send(
                f"Prediction for <{user_recorded[index]}>: {feeling}"
            )
