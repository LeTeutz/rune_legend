import discord
from discord.ext import commands
import json
from bot_func_exclude import Rune
import os
from PIL import Image
import image_generator as img
import io

import image_generator

class Runes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('N-am comanda asta vere.')

    def search(self, champ):
        number = 0
        with open("champions.json", "r") as f:
            dict = json.load(f)
            for name in dict[champ[0].upper()]:
                if champ.upper() == name.upper():
                    return name
                if champ.upper() in name.upper():
                    number += 1
                    result = name
            if number > 1:
                return "X"
            elif number == 1:
                return result
            else:
                return "0"

    @commands.command()
    async def runes(self, ctx, champion, role=''):
        c = self.search(champion)
        if c == 'X':
            await ctx.send('Prea multe variante, mai baga litere')
        elif c == '0':
            await ctx.send('N-am gasit sa moara Garen...')
        else:
            await ctx.send(f'Loading runes for {c}...', delete_after=0)
        c = Rune(c)
        rune_list = c.rune_champ()
        images = img.get_rune_list(rune_list)
        i = img.generate_image(images)

        with io.BytesIO() as image_binary:
            i.save(image_binary, 'PNG')
            image_binary.seek(0)
            print('alo')
            imag = discord.File(fp=image_binary, filename='rune.png')
            embed = discord.Embed(title=f'Runes for {c.champion}', description=f'Skill order: {c.skill_order()}')
            embed.set_thumbnail(url=str(c.get_image()))
            embed.set_image(url='attachment://rune.png')

            await ctx.send(file=imag, embed=embed)

    @commands.command(aliases=['smr'])
    async def _test(self, ctx):
        await ctx.send('smr tu')


def setup(client):
    client.add_cog(Runes(client))
