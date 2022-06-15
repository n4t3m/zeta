
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
import asyncio

from grpc import channel_ready_future

class General(commands.Cog):
    def __init__(self, client):
        self.client = client


    @slash_command(description="Bot Statistics")
    async def stats(self, ctx):
        gcount = len(self.client.guilds)
        memcount = 0
        for g in self.client.guilds:
            try:
                    memcount = memcount + g.member_count
            except:
                pass
        embed=discord.Embed(title="Bot Statistics")
        embed.add_field(name="Guilds", value=str(gcount), inline=False)
        embed.add_field(name="Users", value=str(memcount), inline=False)
        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(General(client))