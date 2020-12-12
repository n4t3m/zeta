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
        embed=discord.Embed()
        embed.add_field(name="Ping", value='Pong! {0}'.format(round(self.bot.latency, 1)))
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        gcount = len(self.bot.guilds)
        memcount = 0
        for g in self.bot.guilds:
            try:
                if member_count > 1000:
                    print(g.name + " " + str(g.member_count))
                    memcount = memcount + g.member_count
            except:
                pass
        embed=discord.Embed(title="Bot Statistics")
        embed.add_field(name="Guilds", value=str(gcount), inline=False)
        embed.add_field(name="Users", value=str(memcount), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Want to invite the bot to your server? Use this link: https://discord.com/oauth2/authorize?client_id=705283045573394493&scope=bot&permissions=270400")

    @commands.command()
    async def tutorial(self, ctx):
        await ctx.send("Want to learn how to use the bot? Watch this video: https://www.youtube.com/watch?v=dHQdAGczV5A")

    @commands.command()
    async def userinfo(self, ctx):
        role_str = ""
        for r in ctx.author.roles:
            role_str += r.name + ", "
        role_str = role_str[:-2]
        embed=discord.Embed(title=f"Information For: {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="ID", value=str(ctx.author.id), inline=True)
        embed.add_field(name="Username", value=ctx.author.name, inline=True)
        embed.add_field(name="Bot", value="False", inline=True)
        embed.add_field(name="Account Creation", value=ctx.author.created_at.strftime("%m/%d/%Y, %H:%M:%S"), inline=True)
        embed.add_field(name="Mention", value=ctx.author.mention, inline=True)
        embed.add_field(name="Roles", value=role_str, inline=True)
        await ctx.send(embed=embed)

    
def setup(bot):
    bot.add_cog(General(bot))