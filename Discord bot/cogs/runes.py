import discord
from discord.ext import commands
import json
#from bot_func_exclude import main
import os
from PIL import Image
import image_generator as img
import io
import time
from refreshing_list import main

import image_generator

class Runes(commands.Cog):

    roles = ["jungle", 'jgl', 'jg', 'mid', 'top', 'bot', 'bottom', 'sup', 'support', 'adc']


    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass
        #self.runesDB = await main()


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

    @commands.command(hidden = True)
    async def alo(self, ctx):
        msg = await ctx.send('[!] MAINTENANCE BREAK')
        await main()
        await msg.delete()

        await ctx.send('[!] BOT WAS UPDATED')


    @commands.command()
<<<<<<< HEAD
    async def runes(self, ctx, champion,* ,role = ''):
        t = time.perf_counter()
        champion = self.search(champion).replace(' ', '')
        print(champion)
        #print(role)
        try:
            if role.split()[-1] in self.roles:
                #print("alo")
                role = role.split()[-1]
            else:
                role = ''
        except Exception as e:
            pass

        await ctx.send(f'Loading runes for {champion} {role}...', delete_after=2)

        with open('runes_dict.json', 'r') as f:
            runesDB = json.load(f)

            #IN CAZ CA NU SE DA UN ROL
            if not role:
                role = list(runesDB[champion].keys())[0]
                c = runesDB[champion][role]
            else:
                c = runesDB[champion][role]



            t2 = time.perf_counter() - t
            print(f"total time pt {champion}: {t2:0.2f}")

            #aici
            rune_list = c['runes']
            images = img.get_rune_list(rune_list)
            i = img.generate_image(images)

            with io.BytesIO() as image_binary:
                i.save(image_binary, 'PNG')
                image_binary.seek(0)

                imag = discord.File(fp=image_binary, filename='rune.png')
                #aici
                embed = discord.Embed(title=f'Runes for {champion} {role}', description=f'Skill order: {c["skills"]}')
                embed.set_thumbnail(url=str(c['image']))
                embed.set_image(url='attachment://rune.png')

                t3 = time.perf_counter() - t
                print(f"total t3 time pt {champion}: {t3:0.2f}")
                await ctx.send(file=imag, embed=embed)

            t4 = time.perf_counter() - t
            print(f"total t4 time pt {champion}: {t4:0.2f}")


=======
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
            embed = discord.Embed(title=f'Runes for {c.champion}', description=f'Skill order: {c.skill_order()}', color=0xffbb00)
            embed.set_thumbnail(url=str(c.get_image()))
            embed.set_image(url='attachment://rune.png')

            await ctx.send(file=imag, embed=embed)
>>>>>>> master

    @commands.command(aliases=['smr'])
    async def test(self, ctx, champion, *, role = ''):
        t = time.perf_counter()
        champion = self.search(champion).replace(' ', '')
        print(champion)
        #print(role)
        try:
            if role.split()[-1] in self.roles:
                #print("alo")
                role = role.split()[-1]
            else:
                role = ''
        except Exception as e:
            pass

        await ctx.send(f'Loading runes for {champion} {role}...', delete_after=3)

        with open('experimental_runes_dict.json', 'r') as f:
            runesDB = json.load(f)

            #IN CAZ CA NU SE DA UN ROL
            if not role:
                role = list(runesDB[champion].keys())[0]
                c = runesDB[champion][role]
            else:
                c = runesDB[champion][role]



            t2 = time.perf_counter() - t
            print(f"total time pt {champion}: {t2:0.2f}")

            #aici
            rune_list = c['runes']
            images = img.get_rune_list(rune_list)
            i = img.generate_image(images)

            with io.BytesIO() as image_binary:
                i.save(image_binary, 'PNG')
                image_binary.seek(0)

                imag = discord.File(fp=image_binary, filename='rune.png')
                #aici
                embed = discord.Embed(title=f'Runes for {champion} {role}', description=f'Skill order: {c["skills"]}')
                embed.set_thumbnail(url=str(c['image']))
                embed.set_image(url='attachment://rune.png')

                t3 = time.perf_counter() - t
                print(f"total t3 time pt {champion}: {t3:0.2f}")
                await ctx.send(file=imag, embed=embed)

            t4 = time.perf_counter() - t
            print(f"total t4 time pt {champion}: {t4:0.2f}")


    @test.error
    async def test_handler(self, ctx, error):
        print(error)

def setup(client):
    client.add_cog(Runes(client))
