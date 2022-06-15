import discord
import os
import config

TOKEN = config.TOK
PREFIX = config.PREFIX
STATUS = config.STATUS
DEFAULT_DELAY = config.DEFAULT_DELAY
DESCRIPTION = config.DESC

bot = discord.Bot()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game(STATUS)
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def load(ctx, extension):
    if ctx.message.author.id != 299685173262286849:
        return 
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    if ctx.message.author.id != 299685173262286849:
        return 
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)