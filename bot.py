# main file for running the bot
import os
import riotAPI as Riot

from discord.ext import commands

# --- Constants ---
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='/')


@bot.command(name='gameinfo')
async def gameinfo(ctx, *args):
    # joining of args necessary because a summoner can consist of multiple words
    await ctx.send(Riot.game_info(" ".join(args[:])))


bot.run(token)
