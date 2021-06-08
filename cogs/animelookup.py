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

    # #Commands
    # @flags.add_flag("--all", action="store_true")
    # @flags.add_flag("--q", nargs="+")
    # @flags.add_flag("--episodes", action="store_true")
    # @flags.add_flag("--synopsis", action="store_true")
    # @flags.add_flag("--page", type=int, default=1)
    # @flags.command()
    # async def animeinfo(self, ctx, **flag):

    #     if flag['q'] == None:
    #         print("h3re")
    #         embed=discord.Embed()
    #         embed.add_field(name="Anime Info", value="Use --q <anime name>. If you want to see episodes, use --episodes. Example: az!animelookup --q k-on!! --episodes --page=2")
    #         await ctx.send(embed=embed)
    #         return
    #     if flag['q'] != None and flag['episodes'] == False and flag['synopsis'] == False:
    #         query = ' '.join(flag['q'])
    #         query = "https://api.jikan.moe/v3/search/anime?q=" + parse.quote(query)
    #         r = requests.get(query)
    #         data = r.json()
    #         if "Error" in data:
    #             await ctx.send("Something Happened, Invalid Request")
    #             return
    #         embed=discord.Embed()
    #         embed.add_field(name="Title", value=data['results'][0]['title'])
    #         embed.set_image(url=data['results'][0]['image_url'])
    #         embed.add_field(name= "MAL Link", value=data['results'][0]['url'], inline=False)
    #         embed.add_field(name= "Episodes", value=data['results'][0]['episodes'])
    #         embed.add_field(name= "Score", value=data['results'][0]['score'])
    #         embed.add_field(name= "Rated", value=data['results'][0]['rated'])
    #         embed.add_field(name= "Synopsis", value=data['results'][0]['synopsis'], inline=False)
    #         await ctx.send(embed=embed)
    #         return
    #     if flag['q'] != None and flag['episodes'] == True:
    #         await ctx.send("Episodes")
    #         query = ' '.join(flag['q'])
    #         query = "https://api.jikan.moe/v3/search/anime?q=" + parse.quote(query)
    #         r = requests.get(query)
    #         data = r.json()
    #         if "Error" in data:
    #             await ctx.send("Something Happened")
    #             return
    #         mal_id = str(data['results'][0]['mal_id'])
    #         title = data['results'][0]['title']
    #         query = f"https://api.jikan.moe/v3/anime/{mal_id}/episodes"
    #         r=requests.get(query)
    #         data = r.json()
    #         episode_str = ""
    #         page_num = flag['page']
    #         pages =  flag['page']

    #         max_page_num = -1

            
    #         if len(data['episodes']) <= 12:
    #             for e in data['episodes']:
    #                 episode_str = episode_str + str(e['episode_id']+1) + ": " + e['title'] + "\n"
    #             episode_str = episode_str.strip()
    #             max_page_num = len(data['episodes'])
    #         else:
    #             if len(data['episodes']) > pages*12:
    #                 if pages*12 <= len(data['episodes']):
    #                     for e in range((pages-1)*12-1, pages*12-1):
    #                         episode_str = episode_str + str(e+1) + ": " + data['episodes'][e]['title'] + "\n"
    #                     if len(data['episodes'])%12==0:
    #                         max_page_num = len(data['episodes'])/12
    #                     else:
    #                         max_page_num = len(data['episodes'])//12 + 1
    #                 else:
    #                     for e in range((pages-1)*12-1, len(data['episodes'])):
    #                         episode_str = episode_str + str(e+1) + ": " + data['episodes'][e]['title'] + "\n"
    #                     max_page_num = page_num
    #             else:
    #                 for e in range((pages-1)*12-1, len(data['episodes'])):
    #                     episode_str = episode_str + str(e+1) + ": " + data['episodes'][e]['title'] + "\n"
    #                 max_page_num = page_num
                    



    #         embed=discord.Embed(title=title)
    #         embed.add_field(name="Episodes", value=episode_str, inline=False)
    #         embed.set_footer(text="Showing Page " + str(page_num) + "/" + str(max_page_num))
    #         await ctx.send(embed=embed)


    #         return

    
def setup(bot):
    bot.add_cog(AnimeInfo(bot))