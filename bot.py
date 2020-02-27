#main file for running the bot
import os
import riot_api_calls

from discord.ext import commands
from dotenv import load_dotenv 

#load discord token from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='/')


@bot.command(name='gameinfo')
async def gameinfo(ctx, *args):

    #joining of args necessary because a summoner can consist of multiple words
    await ctx.send(riot_api_calls.game(" ".join(args[:])))

bot.run(token)