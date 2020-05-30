import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

class Stats(commands.Cog):


    base_url = 'https://www.leagueofgraphs.com/summoner/'

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def stats(self, ctx, region, user):
        html = requests.get(f'{base_url}{region}/{user}')
        page = BeautifulSoup(html, "html.parser")
        print(page)

def setup(client):
    client.add_cog(Stats(client))
