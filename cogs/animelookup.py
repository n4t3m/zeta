import discord
from discord.ext import flags, commands
import requests
from urllib import parse
import os

class AnimeInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Events

    @commands.Cog.listener()
    async def on_ready(self):
        print(os.path.basename(__file__)[:-3].upper() + " loaded succesfully!")

    #Commands
    
    @commands.command()
    async def animeinfo(self, ctx, *, query=None):
        if query == None:
            embed=discord.Embed()
            embed.add_field(name="Anime Info", value="You need to type to include an anime to lookup.")
            await ctx.send(embed=embed)
            return
        query = "https://api.jikan.moe/v3/search/anime?q=" + parse.quote(query)
        r = requests.get(query)
        data = r.json()
        if "Error" in data:
            await ctx.send("Something Happened")
            return
        embed=discord.Embed()
        embed.add_field(name="Title", value=data['results'][0]['title'])
        embed.set_image(url=data['results'][0]['image_url'])
        embed.add_field(name= "MAL Link", value=data['results'][0]['url'], inline=False)
        embed.add_field(name= "Episodes", value=data['results'][0]['episodes'])
        embed.add_field(name= "Score", value=data['results'][0]['score'])
        embed.add_field(name= "Rated", value=data['results'][0]['rated'])
        embed.add_field(name= "Synopsis", value=data['results'][0]['synopsis'], inline=False)
        await ctx.send(embed=embed)

    
def setup(bot):
    bot.add_cog(AnimeInfo(bot))