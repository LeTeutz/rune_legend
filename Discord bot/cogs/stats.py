import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import json

class Stats(commands.Cog):


    summoner_icons_url = 'http://ddragon.leagueoflegends.com/cdn/10.11.1/img/profileicon/'

    def __init__(self, client):
        self.client = client

    def region_mod(self, region):
        with open('./data/regions.json', 'r') as reg:
            reg_list = json.load(reg)
            return reg_list[region]

    def create_summoner_card(self):
        pass

    @commands.command()
    async def stats(self, ctx, region, user):
        region = self.region_mod(region)

        api_key = 'RGAPI-7cb4689c-ac1a-4207-a34f-cf5667d574d5'
        watcher = LolWatcher(api_key)
        player = watcher.summoner.by_name(region, user)
        icons = watcher.data_dragon.profile_icons('10.11.1')
        thumbnail = self.summoner_icons_url + icons['data'][str(player['profileIconId'])]['image']['full']
        embed=discord.Embed(title=f"{player['name']}", description="cel mai cel baiet", color=0xff0000)
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Wrong usage of command \'stats\'", description="\nCorrect usage: `=stats <region> <summoner>`.\n\n\nType `=help stats` for a detailed view of all regions.   ", color=0xff0000)
            await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Stats(client))
