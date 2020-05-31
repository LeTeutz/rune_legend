import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time

base_url = "https://www.op.gg/champion/"

#NU STIU CE FACE DAR MERGE NU ATINGE
class aobject(object):
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a,**kw)
        return instance

    async def __init__(self):
        pass

class Rune(aobject):

    async def __init__(self, champion, rol = ''):

        champion = champion.replace(' ','')
        url = f'{base_url}{champion}/statistics/{rol}'
        #EXPERIMENTAL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                page_url = await response.text()


        page_url = BeautifulSoup(page_url, "html.parser")

        #pagina de baza
        self.img_url = page_url.find("div",{"class":"champion-stats-header-info__image"})
        self.page_url = page_url.find("div",{"class":"l-champion-statistics-content__main"})
        self.champion = champion
        self.rol = rol

    def skill_order(self):
        SKILLS = []
        #skills = self.page_url.find_all("td", {"class":"champion-overview__data"})
        skills = self.page_url.find_all("ul",{"class":"champion-stats__list"})


        try:
            #skills = skills[2].find("ul",{"class":"champion-stats__list"})
            skills_1 = skills[2].find_all("li", {"class":"champion-stats__list__item tip"})
            for skill in skills_1:
                skill = skill.find("span").text
                SKILLS.append(skill)

        except:
            SKILLS = []

            skills_2 = skills[1].find_all("span")
            for skill in skills_2:

                SKILLS.append(skill.text)

        return f"{SKILLS[0]} > {SKILLS[1]} > {SKILLS[2]}"


    def get_image(self):
        img_url = self.img_url.find("img")['src']
        return 'https:' + img_url




    def rune_champ(self):
        RUNE = [[],[],[],[]]


        page_url = self.page_url.find("table",{"class":"champion-overview__table champion-overview__table--rune tabItems"})
        #baga numele paginilor
        nume_pag = page_url.find("div",{"class":"champion-stats-summary-rune__name"}).text.split("+")
        RUNE[0].append(nume_pag[0].strip())
        RUNE[0].append(nume_pag[1].strip())

        rune_page = page_url.find("tbody",{"class":"tabItem ChampionKeystoneRune-1"})
        rune_page = rune_page.find("div",{"class":"perk-page-wrap"})
        runes = rune_page.find_all("div", {"class":"perk-page"})

        #baga runele
        for i,section in enumerate(runes):
            tabs = section.find_all("div",{"class":"perk-page__row"})
            tabs.pop(0)
            for tab in tabs:
                runa = tab.find("div", {"class":"perk-page__item--active"})
                try:
                    runa = runa.find("img")['alt']
                    RUNE[i+1].append(runa)
                except Exception as e:
                    pass

        #baga statsurile
        stats = rune_page.find("div",{"class":"fragment-page"})
        stats = stats.find_all("div",{"class":"fragment__row"})
        for stat in stats:
            try:
                runa = stat.find("img", {"class":"active tip"})["src"]
                RUNE[3].append("https:"+runa)
            except Exception as e:
                pass


        return RUNE


async def main(champ, role):
    tasks = []

    #async with aiohttp.ClientSession() as session:
    # for c in ch:
    #     tasks.append(Rune( c))

    return await Rune(champ, role)
    # a = await asyncio.gather(Rune(session,ch[0]),
    # Rune(session, ch[1])
    # )
    # print(a[0].skill_order())

if __name__ == "__main__":
    t = time.perf_counter()
    #asyncio.run(m(["amumu", "yasuo", "katarina","ekko","gnar","vayne"]))

    test = asyncio.run(main("ekko","jungle"))
    print(test.skill_order())

    t2 = time.perf_counter() - t
    print(f"total time {t2:0.2f}")
