from dalang.discordbot.fetch_messages_from_channel import (
    fetch_messages_from_channel,
)
from dalang.discordbot.helpers import (
    clean_string,
    convert_fetched_messages_to_model_input,
)


async def prepare_channel_messages_for_text_to_mood(ctx, channel_names):
    text_channels = ctx.guild.text_channels
    channel_messages = {}
    if not channel_names:
        text_channels = [text_channel for text_channel in text_channels]
    else:
        channel_names = list(channel_names)
        text_channels = [
            text_channel
            for text_channel in text_channels
            if text_channel.name in channel_names
        ]
    if not text_channels:
        return await ctx.channel.send(f"Channel {channel_name} not found")

    for text_channel in text_channels:
        channel_name = text_channel.name
        msgs = await fetch_messages_from_channel(
            text_channel=text_channel, minutes=None
        )
        channel_messages[channel_name] = msgs

    output_string = convert_fetched_messages_to_model_input(channel_messages)
    output_string = clean_string(output_string)
    # output_string = batch_string(output_string)

    return output_string
