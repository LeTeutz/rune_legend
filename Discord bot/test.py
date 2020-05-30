import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


base_url = 'https://www.leagueofgraphs.com/summoner/'

region = 'eune'
user = 'janelu44'

html = requests.get(f'{base_url}{region}/{user}')
page = BeautifulSoup(html.text, "html.parser")

profile_pic = page.find_all("div", {"class":"img"})
#profile_pic = profile_pic.find("img")["src"]
print(profile_pic)
