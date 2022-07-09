from dotenv import load_dotenv

import dalang.config.configs as config
import dalang.discordbot.commands
import dalang.discordbot.views
from dalang.discordbot.client import bot

load_dotenv()


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")


@bot.event
async def on_message(ctx, message):
    dict = defaultdict(dict)
    dict[ctx.guild.name][message.channel.name] = message
    MessagesDB.add(message)


bot.run(config.DISCORD_TOKEN)
