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
            if message.content.lower() == self.games[str(message.channel.id)][4].lower():
                embed=discord.Embed(title="You Guessed It!", description="Good Job " + message.author.mention + "!", color=0xdd293e)
                embed.add_field(name="The correct word is:", value=self.games[str(message.channel.id)][4].title(), inline=False)
                embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                await message.channel.send(embed=embed)

                del self.games[str(message.channel.id)]
            else:
                if len(message.content) == 1:
                    if message.content.lower() in self.games[str(message.channel.id)][0].lower():

                        if message.content.lower() in self.games[str(message.channel.id)][2].lower():
                            embed=discord.Embed(title="Letter Already Guessed", description="This letter has already been guessed!", color=0xdd293e)
                            embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                            await message.channel.send(embed=embed)
                            return

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
                        embed=discord.Embed(title="Correct!", description=message.author.mention + " has guessed a letter correctly.", color=0xdd293e)
                        embed.add_field(name="Current Progress:", value=self.games[str(message.channel.id)][2], inline=False)
                        embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                        await message.channel.send(embed=embed)




                        if "◯" not in self.games[str(message.channel.id)][2]:

                            #await message.channel.send("**You did it!** The correct word is: " + self.games[str(message.channel.id)][4].title())

                            embed=discord.Embed(title="You Guessed It!", description="Good Job " + message.author.mention + "!", color=0xdd293e)
                            embed.add_field(name="The correct word is:", value=self.games[str(message.channel.id)][4].title(), inline=False)
                            embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                            await message.channel.send(embed=embed)

                            del self.games[str(message.channel.id)]
                    else:
                        #here



                        self.games[str(message.channel.id)][3] = self.games[str(message.channel.id)][3] + 1
                        #await message.channel.send("Incorrect! " + str(message.content) + " is not in the word! Guesses Left: " + str(6-self.games[str(message.channel.id)][3]))

                        embed=discord.Embed(title="Incorrect!", description="Nice Try " + message.author.mention + "!", color=0xdd293e)
                        embed.add_field(name="\'" +str(message.content) + "\'" + " is not in the word!", value="Guesses Left: " + str(6-self.games[str(message.channel.id)][3]), inline=False)
                        embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                        await message.channel.send(embed=embed)


                        if self.games[str(message.channel.id)][3] == 6:
                            #await message.channel.send("You lost :(\n The correct word is: " + self.games[str(message.channel.id)][4].title())

                            embed=discord.Embed(title="You Lost :(", description="You have run out of guesses.", color=0xdd293e)
                            embed.add_field(name="The correct word is:", value=self.games[str(message.channel.id)][4].title(), inline=False)
                            embed.set_footer(text="Hangman - Category: " + self.games[str(message.channel.id)][1].title())
                            await message.channel.send(embed=embed)

                            del self.games[str(message.channel.id)]
                            

    #Commands
    
    @commands.command()
    async def hangman(self, ctx, *, arg=None):
        if arg!=None and arg.lower() == "categories":
            categs = ""
            for x in self.words:
                categs = categs + x.title() + "\n"

            embed=discord.Embed(title="Categories", description=categs.strip(), color=0xdd293e)
            embed.set_footer(text="Hangman - Zeta Bot")
            await ctx.send(embed=embed)
            return

        #Create Game Instance
        if str(ctx.channel.id) not in self.games:
            random_category = False
            category = ""
            if(arg==None):
                category = random.choice(list(self.words))
                random_category = True
            else:
                if arg.lower() in self.words:
                    category = arg.lower()
                else:
                    embed=discord.Embed(title="Invalid Category", description= arg + " is not a valid category! To see all categories, type ``<prefix>hangman categories``!", color=0xdd293e)
                    embed.set_footer(text="Hangman - Zeta Bot")
                    await ctx.send(embed=embed)
                    return
            word = random.choice(self.words[category])
            unchanged_word=word

            if random_category:
                embed=discord.Embed(title="Starting a Game of Hangman", description="Random Category: " + category.title(), color=0xdd293e)
                embed.set_footer(text="Hangman - Category: " + category.title())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Starting a Game of Hangman", description="Selected Category: " + category.title(), color=0xdd293e)
                embed.set_footer(text="Hangman - Category: " + category.title())
                await ctx.send(embed=embed)

            guess_str = "```"
            for x in word:
                if x == " ":
                    guess_str+="  "
                else:
                    guess_str+="◯ "
            guess_str = guess_str + "```"

            temp_str = ""
            for letter in word:
                temp_str = temp_str + letter + " "
            guess_str=guess_str.strip()
            word = temp_str
            word = word.strip()
            self.games[str(ctx.channel.id)] = ["```" + word.lower() + "```",category.title(), guess_str, 0, unchanged_word]
            #print(self.games)
        
        #Send Game Progress
        await ctx.channel.send(self.games[str(ctx.channel.id)][2])


    
    
def setup(bot):
    bot.add_cog(Hangman(bot))