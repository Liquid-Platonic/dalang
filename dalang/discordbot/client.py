from typing import Optional

from discord import Guild, Intents, VoiceClient
from discord.ext import commands

intents = Intents.all()

bot = commands.Bot(command_prefix="/", intents=intents)


def find_voice_client(guild: Guild) -> Optional[VoiceClient]:
    for voice_client in bot.voice_clients:
        if voice_client.guild == guild:
            return voice_client
    return None
