import asyncio
import aiohttp
from rune_scraper import Rune
import json
import time
#from experimental_runes_dict import RUNES_DICT

runesDB = {}
BASE_URL = "https://www.op.gg/champion/"

async def download_rune_page(url):
    print(f'started downloading {url}')
    async with aiohttp.ClientSession() as session:
        async with  session.get(url) as resp:
            content = await resp.text()
            print(f'finished requesting {url}')
            return content

async def add_to_rune_list(champ, content, role):
    #champion =  Rune(champ, content)
    #runesDB[champ] = {}
    #for role in champion.get_roles():
    ch = Rune(champ, content, role)
    runesDB[champ][role] = {}
    print(f'creating object for {champ} {role}')
    runesDB[champ][role]['skills'] = ch.skill_order()
    runesDB[champ][role]['runes'] = ch.rune_champ()
    runesDB[champ][role]['image'] = ch.get_image()
    print(f'finished object for {champ} {role}')

async def scrape_task(url, champ):
    try:
        runesDB[champ] = {}
        content = await download_rune_page(url)
        roles = Rune(champ,content)
        roles = roles.get_roles()
        await add_to_rune_list(champ, content, roles[0])
        if len(roles) > 1:
            content = await download_rune_page(f'{url}{roles[1]}')
            await add_to_rune_list(champ, content, roles[1])
        # if len(roles) > 2:
        #     content = await download_rune_page(f'{url}{roles[2]}')
        #     await add_to_rune_list(champ, content, roles[2])
    except Exception as e:
        print("BUNAAAAAAAAAAAAAAAA")
        print(e)

async def main():
    tasks = []
    t = time.perf_counter()
    with open("champions.json", 'r') as data:
        data = json.load(data)
        for i in data.values():
            for j in i:
                j = j.replace(' ','')
                url = f'{BASE_URL}{j}/statistics/'
                tasks.append(scrape_task(url, j))
        await asyncio.wait(tasks)

    #ATENTIE SANTIER
    # del tasks
    # tasks = []
    # for chmp, run in runesDB.items():
    #     if len(run) == 0:
    #         print(f'ALOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO {chmp}')
    #         chmp = chmp.replace(' ', '')
    #         url = f'{BASE_URL}{j}/statistics/'
    #         tasks.append(scrape_task(url, chmp))
    #
    # if len(tasks) > 0:
    #     await asyncio.wait(tasks)


    with open("runes_dict.json", 'w') as file:
        json.dump(runesDB, file)
    t2 = time.perf_counter() - t
    print(f'total time take: {t2:0.2f} seconds')





if __name__ == '__main__':
    pass
