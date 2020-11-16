import discord
from discord.ext import commands
import random
import asyncio
import config
import os

class Hangman(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.PREFIX
        self.games={}

    #Events

    @commands.Cog.listener()
    async def on_ready(self):
        print(os.path.basename(__file__)[:-3].upper() + " loaded succesfully!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.id) in self.games:
            if message.content.lower() == self.games[str(message.channel.id)][0].lower():
                await message.channel.send("Correct! The word was " + self.games[str(message.channel.id)][0])
                del self.games[str(message.channel.id)]
            else:
                if len(message.content) == 1:
                    if message.content in self.games[str(message.channel.id)][0] and message.content not in self.games[str(message.channel.id)][2]:
                        indexes = []
                        for n in range(0,len(self.games[str(message.channel.id)][0])):
                            if self.games[str(message.channel.id)][0][n]==message.content:
                                indexes.append(n)
                        temp = ""
                        for i in range(0, len(self.games[str(message.channel.id)][2])):
                            if i in indexes:
                                temp = temp + message.content
                            else:
                                temp = temp + self.games[str(message.channel.id)][2][i]
                            self.games[str(message.channel.id)][2] = self.games[str(message.channel.id)][2]

                        self.games[str(message.channel.id)][2]=temp
                        await message.channel.send("Correct!\n" + self.games[str(message.channel.id)][2])
                        if "_" not in self.games[str(message.channel.id)][2]:
                            await message.channel.send("**You did it!** The correct word is: " + self.games[str(message.channel.id)][2])
                            del self.games[str(message.channel.id)]
                    else:
                        self.games[str(message.channel.id)][3] = self.games[str(message.channel.id)][3] + 1
                        await message.channel.send("Incorrect! " + str(message.content) + " is not in the word! Guesses Left: " + str(6-self.games[str(message.channel.id)][3]))
                        if self.games[str(message.channel.id)][3] == 6:
                            await message.channel.send("You lost :(\n The correct word is: " + self.games[str(message.channel.id)][0])
                            del self.games[str(message.channel.id)]
                            

    #Commands
    
    @commands.command()
    async def hangman(self, ctx):


        #Create Game Instance
        if ctx.guild.id not in self.games:
            await ctx.send("Starting a game of hangman...")
            word = "word"
            category = "category"
            guess_str = "```"
            for x in word:
                guess_str+="_"
            guess_str = guess_str + "```"
            guess_str=guess_str.strip()
            self.games[str(ctx.channel.id)] = ["```word```", "category", guess_str, 0]
            print(self.games)
        
        #Send Game Progress
        await ctx.channel.send(self.games[str(ctx.channel.id)][2])


    
    
def setup(bot):
    bot.add_cog(Hangman(bot))