import discord
from discord.ext import commands
import random
import asyncio
import config
import os
import json
import random

class Hangman(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.PREFIX
        self.games={}
        with open('./hangman_data/words.json') as json_file:
            self.words = json.load(json_file)

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
                    if message.content.lower() in self.games[str(message.channel.id)][0].lower() and message.content not in self.games[str(message.channel.id)][2]:
                        indexes = []
                        for n in range(0,len(self.games[str(message.channel.id)][0])):
                            if self.games[str(message.channel.id)][0][n].lower()==message.content.lower():
                                indexes.append(n)
                        temp = ""
                        for i in range(0, len(self.games[str(message.channel.id)][2])):
                            if i in indexes:
                                temp = temp + message.content.lower()
                            else:
                                temp = temp + self.games[str(message.channel.id)][2][i]
                            self.games[str(message.channel.id)][2] = self.games[str(message.channel.id)][2]

                        self.games[str(message.channel.id)][2]=temp
                        await message.channel.send("Correct!\n" + self.games[str(message.channel.id)][2])
                        #fixme

                        if "_" not in self.games[str(message.channel.id)][2]:
                            await message.channel.send("**You did it!** The correct word is: " + self.games[str(message.channel.id)][2].title())
                            del self.games[str(message.channel.id)]
                    else:
                        self.games[str(message.channel.id)][3] = self.games[str(message.channel.id)][3] + 1
                        await message.channel.send("Incorrect! " + str(message.content) + " is not in the word! Guesses Left: " + str(6-self.games[str(message.channel.id)][3]))
                        if self.games[str(message.channel.id)][3] == 6:
                            await message.channel.send("You lost :(\n The correct word is: " + self.games[str(message.channel.id)][0].title())
                            del self.games[str(message.channel.id)]
                            

    #Commands
    
    @commands.command()
    async def hangman(self, ctx, *, arg=None):



        #Create Game Instance
        if str(ctx.channel.id) not in self.games:
            random_category = False
            category = ""
            if(arg==None):
                category = random.choice(list(self.words))
                random_category = True
            else:
                if category.lower() in self.words:
                    category = args
                else:
                    await ctx.send(arg + " is not a valid category! To see all categories, type this command that is not implemented yet!")
                    return
            word = random.choice(self.words[category])

            if random_category:
                await ctx.send("Starting a game of hangman. Random Category: " + category.title())
            else:
                await ctx.send("Starting a game of hangman. Selected Category: " + category.title())

            guess_str = "```"
            for x in word:
                if x == " ":
                    guess_str+=" "
                else:
                    guess_str+="_"
            guess_str = guess_str + "```"
            guess_str=guess_str.strip()
            self.games[str(ctx.channel.id)] = ["```" + word.lower() + "```",category.title(), guess_str, 0]
            print(self.games)
        
        #Send Game Progress
        await ctx.channel.send(self.games[str(ctx.channel.id)][2])


    
    
def setup(bot):
    bot.add_cog(Hangman(bot))