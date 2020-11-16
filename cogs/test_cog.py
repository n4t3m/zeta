import discord
from discord.ext import commands

class General(commands.Cog):

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

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Want to invite the bot to your server? Use this link: https://discord.com/oauth2/authorize?client_id=705283045573394493&scope=bot&permissions=270400")

    @commands.command()
    async def tutorial(self, ctx):
        await ctx.send("Want to learn how to use the bot? Watch this video: https://www.youtube.com/watch?v=dHQdAGczV5A")

    
def setup(bot):
    bot.add_cog(General(bot))