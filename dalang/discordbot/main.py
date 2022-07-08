from dotenv import load_dotenv

import dalang.config.configs as config
from dalang.discordbot.client import bot

load_dotenv()


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")


bot.run(config.DISCORD_TOKEN)
