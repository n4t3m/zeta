import discord
from discord.ext import commands
import random
import json
import asyncio
import config
import os

class AutoPrune(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.PREFIX

    #Events

    @commands.Cog.listener()
    async def on_ready(self):
        print(os.path.basename(__file__)[:-3].upper() + " loaded succesfully!")

    @commands.Cog.listener()
    async def on_message(self, message):
        
        with open('./ap_data/guilds.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(message.guild.id) not in data:
            return

        with open('./ap_data/delays.json') as json_file:
            existingData = json.load(json_file)
        t_data = existingData
        
        if message.content.lower().startswith("az!ignore") and message.author.guild_permissions.administrator:
            return

        if str(message.channel.id) in t_data:
            d = t_data[str(message.channel.id)]
            await self.remove_msg(message, d)
            return

    #Commands
    
    @commands.command()
    async def addChannel(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You must be administrator to use this command")
            return

        with open('./ap_data/guilds.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = []

        if ctx.message.channel.id not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)].append(ctx.message.channel.id)
        else:
            print("This channel already has pruning enabled. Use the remove command in this channel if you would like to remove it.")
        

        await ctx.send("Added " + ctx.message.channel.name + " to pruned channels. Use the channels command to see which channels are being pruned.")

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)
        
        with open('./ap_data/delays.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.channel.id) not in data:
            data[str(ctx.channel.id)] = 300

        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    @commands.command()
    async def channels(self, ctx):

        with open('./ap_data/guilds.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.guild.id) not in data:
            await ctx.send("This server has not been configured! Use the command ``addChannel`` to start pruning new messages!")
            return
        

        if len(data[str(ctx.guild.id)])==0:
            await ctx.send("This server has no channels configured!")
            return

        message = "Channels Being Pruned: "

        for x in data[str(ctx.guild.id)]:
            try:
                channel = self.bot.get_channel(x)
                message = message + channel.name + ", "
            except:
                pass

        message = message[:-2]

        await ctx.send(message)
        await ctx.send("Unfortunately all data has been lost (11/1). Please reconfigure your servers to keep using the bot. When you set a delay, that delay only applies to one specific channel, so you must set the delay for each channel you want to use the bot with.")

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)

    @commands.command()
    async def remove(self, ctx):

        with open('./ap_data/guilds.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.guild.id) not in data:
            await ctx.send("This server has no channels configured!")
            return

        if ctx.message.channel.id not in data[str(ctx.guild.id)]:
            await ctx.send("Channel cannot be removed as messages are not being removed here!")
            return

        data[str(ctx.guild.id)].remove(ctx.message.channel.id)

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)

        with open('./ap_data/delays.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.channel.id) not in data:
            await ctx.send("This channel has not been configured!")
            return

        del data[str(ctx.channel.id)]
        
        await ctx.send("Removed channel: " + ctx.channel.name)

        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)


    @commands.command()
    async def delay(self, ctx, d: int):
        with open('./ap_data/delays.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        data[str(ctx.channel.id)] = d

        await ctx.send("New Channel Delay Set: " + str(data[str(ctx.channel.id)]) + " seconds. Delays are now specific to channels. In each channel you want to prune in, you must set the delay using the delay command.")

        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    @commands.command()
    async def checkdelay(self, ctx):
        with open('./ap_data/delays.json') as json_file:
            existingData = json.load(json_file)
        data = existingData

        if str(ctx.channel.id) not in data:
            data[str(ctx.channel.id)] = 300
        
        await ctx.send("Current Channel's Delay: " + str(data[str(ctx.channel.id)]) + " seconds." )
        
        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    async def remove_msg(self, message, delay):
        c_name = message.channel.name
        g_name = message.guild.name
        await asyncio.sleep(delay) 
        await message.delete()
        print("A message has been automatically pruned in " + c_name + " in the server " + g_name)
        return

    @commands.command()
    async def ignore(self, ctx):
        return

    
    
def setup(bot):
    bot.add_cog(AutoPrune(bot))
