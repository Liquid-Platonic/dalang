from discord import Message
from discord.ext.commands import Context
from dotenv import load_dotenv

import dalang.config.configs as config
import dalang.discordbot.commands
import dalang.discordbot.views
from dalang.discordbot.client import bot
from dalang.discordbot.db import message_db

load_dotenv()


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")


@bot.event
async def on_message(message: Message):
    message_db(message.guild).add(message)
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)


bot.run(config.DISCORD_TOKEN)
