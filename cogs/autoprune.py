
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json

class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Get the ID of a user")
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(f"The ID of {user} is {user.id}")

    @slash_command(
        name="addchannel",
        description="Let this channel be pruned"
        )
    async def addchannel(self, ctx, channel: Option(discord.TextChannel, "Channel", required=True)):
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

def setup(client):
    client.add_cog(Cog(client))