import discord
from discord.ext import commands

class Test_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Events

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online!")

    #Commands
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {0}'.format(round(self.bot.latency, 1)))
        await ctx.send("Unfortunately all data has been lost (11/1). Please reconfigure your servers to keep using the bot. When you set a delay, that delay only applies to one specific channel, so you must set the delay for each channel you want to use the bot with.")

    @commands.command()
    async def stats(self, ctx):
        gcount = len(self.bot.guilds)
        memcount = 0
        for g in self.bot.guilds:
            try:
                print(g.name + " " + str(g.member_count))
                memcount = memcount + g.member_count
            except:
                pass
        await ctx.send("Guilds: " + str(gcount) + "\nMembers: " + str(memcount))

    
def setup(bot):
    bot.add_cog(Test_Cog(bot))