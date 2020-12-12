import discord
from discord.ext import commands
import random
import asyncio
import config
import os
import json
import random

class Trivia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.PREFIX
        self.games={}
        with open('./trivia_data/questions.json') as json_file:
            self.questions = json.load(json_file)

    #Events

    @commands.Cog.listener()
    async def on_ready(self):
        print(os.path.basename(__file__)[:-3].upper() + " loaded succesfully!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.id) in self.games:
            if message.content.lower() == self.games[str(message.channel.id)][1].lower():
                embed=discord.Embed(title="You Got It!", description="Good Job " + message.author.mention + "!", color=0xdd293e)
                embed.add_field(name="The correct answer is:", value=self.games[str(message.channel.id)][1].title(), inline=False)
                #embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                await message.channel.send(embed=embed)
                del self.games[str(message.channel.id)]                          

    #Commands
    
    @commands.command()
    async def trivia(self, ctx, *, arg=None):
        if arg!=None and arg.lower() == "categories":
            categs = ""
            for x in self.questions:
                categs = categs + x.title() + "\n"
            embed=discord.Embed(title="Categories", description=categs.strip(), color=0xdd293e)
            embed.set_footer(text="Trivia - Zeta Bot")
            await ctx.send(embed=embed)
            return

        #Create Game Instance
        if str(ctx.channel.id) not in self.games:
            random_category = False
            category = ""
            if(arg==None):
                category = random.choice(list(self.questions))
                random_category = True
            else:
                if arg.lower() in self.questions:
                    category = arg.lower()
                else:
                    embed=discord.Embed(title="Invalid Category", description= arg + " is not a valid category! To see all categories, type ``<prefix>trivia categories``!", color=0xdd293e)
                    embed.set_footer(text="Trivia - Zeta Bot")
                    await ctx.send(embed=embed)
                    return
            question = random.choice(self.questions[category])

            if random_category:
                embed=discord.Embed(title=question[0], description="Random Category: " + category.title(), color=0xdd293e)
                embed.set_footer(text="Trivia - Category: " + category.title())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=question[0], description="Selected Category: " + category.title(), color=0xdd293e)
                embed.set_footer(text="Trivia - Category: " + category.title())
                await ctx.send(embed=embed)
            self.games[str(ctx.channel.id)] = question
        else:
            await ctx.send("Game Already in Progress")


    
    
def setup(bot):
    bot.add_cog(Trivia(bot))