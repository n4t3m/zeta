import discord
import os
from discord.ext import commands
import config

TOKEN = config.TOK
PREFIX = config.PREFIX
STATUS = config.STATUS
DEFAULT_DELAY = config.DEFAULT_DELAY
DESCRIPTION = config.DESC

bot = commands.Bot(command_prefix=PREFIX, description=DESCRIPTION, case_insensitive=True)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game(STATUS)
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(TOKEN)