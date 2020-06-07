import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time
import requests

BASE_URL = "https://www.op.gg/champion/"


class Rune(object):

    def __init__(self,champion, content , rol = ''):

        champion = champion.replace(' ','')
        # url = f'{BASE_URL}{champion}/statistics/{rol}'
        # content = requests.get(url)
        self.base_url = BeautifulSoup(content, "html.parser")
        #pagina de baza

        self.page_url = self.base_url.find("div",{"class":"l-champion-statistics-content__main"})
        self.champion = champion
        self.rol = rol

    def get_roles(self):
        #try:
        ROLES = []
        roles = self.base_url.find_all("li",{"class":"champion-stats-header__position"})
        for role in roles:
            ROLES.append(role["data-position"].lower())
        return ROLES

        # except :
        #     print("CRAPA PIZDA MA SII")

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
        img_url = self.base_url.find("div",{"class":"champion-stats-header-info__image"})
        img_url = img_url.find("img")['src']
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




if __name__ == "__main__":
    t = time.perf_counter()
    #asyncio.run(m(["amumu", "yasuo", "katarina","ekko","gnar","vayne"]))

    test = Rune(champion = "evelynn")
    print(test.get_roles())
    print(test.rune_champ())
    print(test.skill_order())
    t2 = time.perf_counter() - t
    print(f"total time {t2:0.2f}")
