import wave
from pathlib import Path

import discord
from discord.sinks import Sink

from dalang.models.distilbert import text_to_mood_model
from dalang.models.speech2text import speech_to_text_model


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


async def find_mood_from_recordings(
    sink: Sink, channel: discord.TextChannel, *args
):  # Our voice client already passes these in.
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

    # predictions = [
    #     speech_to_mood_model.predict(Path(file).absolute())
    #     for file in filepaths
    # ]
    texts = [
        speech_to_text_model.predict(Path(file).absolute())
        for file in filepaths
    ]
    predictions = [
        text_to_mood_model.predict(' '.join(text))
        for text in texts
    ]

    for index, prediction in enumerate(predictions):
        feeling = max(
            [
                {"mood": key, "value": value}
                for key, value in prediction.items()
            ],
            key=lambda x: x["value"],
        )
        await channel.send(
            f"Prediction for <{user_recorded[index]}> :{feeling}\n Text: {texts[index]}"
        )
