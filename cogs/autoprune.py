
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
import asyncio

from grpc import channel_ready_future

class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        
        print('msg detected')

    @slash_command(description="Get the ID of a user")
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(f"The ID of {user} is {user.id}")

    @slash_command(
        name="addchannel",
        description="Select a channel to prune messages in."
        )
    async def addchannel(self, ctx, channel: Option(discord.TextChannel, "Channel to prune messages in", required=True)):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You must be administrator to use this command", ephemeral=True)
            return

        #channel = channel or ctx.channel
        cid = channel.id
        gid = channel.guild.id

        with open('./ap_data/guilds.json') as json_file:
            data = json.load(json_file)

        if str(gid) not in data:
            data[str(gid)] = []

        if cid not in data[str(gid)]:
            data[str(gid)].append(cid)
        else:
            await ctx.respond("This channel already has pruning enabled. Use the remove command in this channel if you would like to remove it.")
            return

        await ctx.respond(f"Added {channel.name} to pruned channels. Use the channels command to see which channels are being pruned.")

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)
        
        with open('./ap_data/delays.json') as json_file:
            data = json.load(json_file)

        if str(cid) not in data:
            data[str(cid)] = 300

        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    @slash_command(
        name="channels",
        description="List all channels being pruned in this server."
        )
    async def channels(self, ctx):

        with open('./ap_data/guilds.json') as json_file:
            data = json.load(json_file)

        gid = ctx.guild.id

        if str(gid) not in data:
            await ctx.respond("This server has not been configured! Use the command ``/addChannel`` to start pruning new messages!", ephemeral=True)
            return

        if len(data[str(gid)])==0:
            await ctx.respond("This server has no channels configured!", ephemeral=True)
            return

        message = "Channels Being Pruned: "

        for x in data[str(gid)]:
            try:
                channel = self.client.get_channel(int(x))
                message = message + channel.name + ", "
            except:
                print('something happened here"')
                pass

        message = message[:-2]

        if len(data[str(gid)]) == 0:
            message = message + "\nNone"

        await ctx.respond(message, ephemeral=True)

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)

    @slash_command(
        name="remove",
        description="Select a channel to remove pruning in"
        )
    async def remove(self, ctx, channel: Option(discord.TextChannel, "Channel", required=True)):
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You must be administrator to use this command", ephemeral=True)
            return

        with open('./ap_data/guilds.json') as json_file:
            data = json.load(json_file)


        gid = ctx.guild.id
        cid = ctx.channel.id

        if str(gid) not in data:
            await ctx.respond("No messages are being removed in this channel.", ephemeral=True)
            return

        if cid not in data[str(gid)]:
            await ctx.respond("No messages are being removed in this channel", ephemeral=True)
            return

        data[str(gid)].remove(cid)

        with open("./ap_data/guilds.json", "w") as write_file:
            json.dump(data, write_file)

        with open('./ap_data/delays.json') as json_file:
            data = json.load(json_file)

        if str(cid) not in data:
            await ctx.respond("This channel has not been configured!", ephemeral=True)
            return

        del data[str(cid)]
        
        await ctx.respond(f"Removed channel: {ctx.channel.name}", ephemeral=True)

        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    @slash_command(
        name="setdelay",
        description="Set the delay before messages are deleted in a channel")
    async def setdelay(self, ctx, delay: Option(int, "Number of seconds that should be waited before deleting a message.", required=True)):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You must be administrator to use this command", ephemeral=True)
            return

        with open('./ap_data/delays.json') as json_file:
            data = json.load(json_file)

        data[str(ctx.channel.id)] = delay

        await ctx.respond(f"New Channel Delay for {ctx.channel.name} Set: {str(data[str(ctx.channel.id)])} seconds.", ephemeral=True)
        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)

    @slash_command(
        name="checkdelay",
        description="Check the current delay for a specified channel.")
    async def checkdelay(self, ctx,  channel: Option(discord.TextChannel, "Channel", required=False)):

        with open('./ap_data/delays.json') as json_file:
            data = json.load(json_file)

        channel = channel or ctx.channel

        cid = channel.id

        if str(cid) not in data:
            await ctx.respond(f"{channel.name}'s messages are not being pruned. Use /addchannel to prune messages in a channel", ephemeral=True)
            return
        
        await ctx.respond(f"{channel.name}'s Current Delay: {str(data[str(cid)])} seconds.", ephemeral=True)
        
        with open("./ap_data/delays.json", "w") as write_file:
            json.dump(data, write_file)



    async def remove_msg(self, message, delay):
        c_name = message.channel.name
        g_name = message.guild.name
        await asyncio.sleep(delay) 
        await message.delete()
        print("A message has been automatically pruned in " + c_name + " in the server " + g_name)
        return


def setup(client):
    client.add_cog(Cog(client))