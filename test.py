"""
from riotAPI import *

print(game_info("geldin"))
"""
# TOKEN = os.getenv('DISCORD_TOKEN')
# ---   Libs    ---
import discord
import os

# --- Constants ---
TOKEN = os.getenv('DISCORD_TOKEN')


# Bot client class, to manage the bot
class BotClient(discord.Client):
    # Login message
    async def on_ready(self):
        print("eSportBot has connected.")

    async def on_message(self, message):
        if message.author == client:
            return
        print("Message from " + str(message.author) + " enthält " + str(message.content))


# Start eSportBot
client = BotClient()
client.run(TOKEN)
