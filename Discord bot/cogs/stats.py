import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import json

class Stats(commands.Cog):


    summoner_icons_url = 'http://ddragon.leagueoflegends.com/cdn/10.11.1/img/profileicon/'

    def __init__(self, client):
        self.client = client

    def get_api(self):
        with open('config.json', 'r') as f:
            dict = json.load(f)
            return dict["api_key"]


    def region_mod(self, region):
        with open('./data/regions.json', 'r') as reg:
            reg_list = json.load(reg)
            return reg_list[region]

    def create_summoner_card(self, summoner, thumbnail, ranks):

        embed=discord.Embed(title=f"{summoner['name']}", description=f"Level {summoner['summonerLevel']}", color=0x018aad)
        embed.set_thumbnail(url=thumbnail)

        flex_rank = 'Unranked'
        solo_rank = 'Unranked'

        for mode in ranks:
            try:
                if mode['queue_type'] == 'RANKED_FLEX_SR':
                    flex_rank = f"{mode['tier'].title()} {mode['rank']}"
            except:
                pass

            try:
                if mode['queue_type'] == 'RANKED_SOLO_5x5':
                    solo_rank = f"{mode['tier'].title()} {mode['rank']}"
            except:
                pass

        embed.add_field(name="Solo Rank", value=solo_rank, inline=True)
        embed.add_field(name="Flex Rank", value=flex_rank, inline=True)

        return embed


    @commands.command()
    async def stats(self, ctx, region, user):
        region = self.region_mod(region)
        api = self.get_api()
        watcher = LolWatcher(api)

        try:
            summoner = watcher.summoner.by_name(region, user)
            icons = watcher.data_dragon.profile_icons('10.11.1')
            thumbnail = self.summoner_icons_url + icons['data'][str(summoner['profileIconId'])]['image']['full']

            ranks = [{}, {}]

            r = watcher.league.by_summoner(region, summoner['id'])

            for i in range(2):
                try:
                    ranks[i]['queue_type'] = r[i]['queueType']
                    ranks[i]['tier'] = r[i]['tier']
                    ranks[i]['rank'] = r[i]['rank']
                except:
                    pass

            embed = self.create_summoner_card(summoner, thumbnail, ranks)
            await ctx.send(embed=embed)

        except Exception as e:
            if str(e).split(' ')[0] == '404':
                await ctx.send('This summoner does not exist in the specified region')

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Wrong usage of command \'stats\'", description="\nCorrect usage: `=stats <region> <summoner>`.\n\n\nType `=help stats` for a detailed view of all regions.   ", color=0xff0000)
            await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Stats(client))
