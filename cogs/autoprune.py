import discord
from discord.ext import commands
import random
import json
import asyncio
import config
import os
from pymongo import MongoClient

class AutoPrune(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.PREFIX
        self.connection = MongoClient("mongodb://localhost")
        self.db = self.connection["zeta"]
        self.collection = self.db["autoprune"]

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
        
        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            self.collection.insert_one({
                "_id": str(ctx.channel.id),
                "guild": str(ctx.guild.id),
                "delay": config.DEFAULT_DELAY,
                "created_by": ctx.message.author.name,
                "attatchment_only": False,
                "bot_only": False
                })
        else:
            await ctx.channel.send("Channel is already being pruned.")
            return
        
        await ctx.channel.send("Success!")

    @commands.command()
    async def channels(self, ctx):
        results = self.collection.find({"guild": str(ctx.guild.id)})
        resp = "===Channels Being Pruned===\n"

        for entry in results:
            try:
                c = self.bot.get_channel(int(entry['_id']))
                resp+= f"{c.mention}\n"
            except:
                self.collection.delete_one(entry)

        await ctx.channel.send(resp.strip()) 

    @commands.command()
    async def channelinfo(self, ctx):
        results = self.collection.find({"guild": str(ctx.guild.id)})
        resp = "===Channels Being Pruned===\n"

        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Cannot show results as {ctx.channel.name} is not being pruned.")
            return


        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if r:
            await ctx.send(str(r))
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return

    @commands.command()
    async def remove(self, ctx):

        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You must be administrator to use this command")
            return

        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Nothing happened as {ctx.channel.name} was not being pruned in the first place.")
            return

        r = self.collection.delete_one({"_id": str(ctx.channel.id)})

        if r.acknowledged:
            await ctx.send(f"{ctx.channel.name} will no longer be pruned.")
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return


    @commands.command()
    async def delay(self, ctx, d: int):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You must be administrator to use this command")
            return

        if d>86400:
            await ctx.send("The maximum delay is set to 1 day because people like to abuse the bot.")
            return

        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Nothing happened as {ctx.channel.name} was not being pruned in the first place.")
            return

        r = self.collection.update_one( {"_id": str(ctx.channel.id)}, {"$set": {"delay": d}}  )

        if r.acknowledged:
            await ctx.send(f"Updated AutoPrune delay to {d} seconds.")
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return

    @commands.command()
    async def togglebot(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You must be administrator to use this command")
            return

        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Nothing happened as {ctx.channel.name} was not being pruned in the first place.")
            return

        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if not r:
            await ctx.channel.send("Something bad happened")
            return

        update_r = self.collection.update_one( {"_id": str(ctx.channel.id)}, {"$set": {"bot_only": not r['bot_only']}}  )

        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if update_r.acknowledged:
            r = self.collection.find_one( {"_id": str(ctx.channel.id)} )
            if r:
                if r['bot_only']:
                    return await ctx.send("Only messages from bots will now be pruned.")
                else:
                    return await ctx.send("Messages from all types of users will now be pruned.")
            else:
                await ctx.send("Something bad happened")
                return
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return

    @commands.command()
    async def toggleattachments(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You must be administrator to use this command")
            return

        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Nothing happened as {ctx.channel.name} was not being pruned in the first place.")
            return

        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if not r:
            await ctx.channel.send("Something bad happened")
            return

        update_r = self.collection.update_one( {"_id": str(ctx.channel.id)}, {"$set": {"attatchment_only": not r['attatchment_only']}}  )

        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if update_r.acknowledged:
            r = self.collection.find_one( {"_id": str(ctx.channel.id)} )
            if r:
                if r['attatchment_only']:
                    return await ctx.send("Only messages with attachments will be pruned.")
                else:
                    return await ctx.send("All types of messages will be pruned.")
            else:
                await ctx.send("Something bad happened")
                return
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return


    @commands.command()
    async def checkdelay(self, ctx):
        if self.collection.count_documents( {"_id": str(ctx.channel.id)} ) == 0:
            await ctx.send(f"Nothing happened as {ctx.channel.name} was not being pruned in the first place (so there is no delay).")
            return
        
        r = self.collection.find_one( {"_id": str(ctx.channel.id)} )

        if r:
            await ctx.send(f"Delay in {ctx.channel.name} is {r['delay']} seconds.")
            return
        else:
            await ctx.send("Something bad happened. Please join the official server and report this to the developer. https://discord.gg/4e25RDd")
            return



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

    # @commands.command()
    # async def test_fake_data_enterdb(self, ctx):
    #     try:
    #         self.collection.insert_one({
    #             "_id": str(ctx.message.id),
    #             "content": ctx.message.content,
    #             "author": ctx.message.author.name,
    #             "a new field that others will not have": "poggers"
    #         })
    #     except:
    #         await ctx.channel.send("wwww")

def setup(bot):
    bot.add_cog(AutoPrune(bot))
