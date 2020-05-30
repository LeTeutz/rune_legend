import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio

base_url = "https://www.op.gg/champion/"


class Rune:

    def __init__(self, champion, rol = ''):

        champion = champion.replace(" ",'')
        page_url = requests.get(f"{base_url}{champion}/statistics/{rol}")
        page_url = BeautifulSoup(page_url.content, "html.parser")
        #pagina de baza
        self.img_url = page_url.find("div",{"class":"champion-stats-header-info__image"})
        self.page_url = page_url.find("div",{"class":"l-champion-statistics-content__main"})
        self.champion = champion
        self.rol = rol

    def skill_order(self):
        SKILLS = []
        skills = self.page_url.find_all("td", {"class":"champion-overview__data"})[2]
        skills = skills.find("ul",{"class":"champion-stats__list"})
        skills = skills.find_all("li", {"class":"champion-stats__list__item tip"})

        for skill in skills:
            skill = skill.find("span").text
            SKILLS.append(skill)
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

        #asta merge ignorat/scos
        # for ind,i in enumerate(RUNE):
        #     while len(i) < 4:
        #         RUNE[ind].append("")

        return RUNE



if __name__ == "__main__":
    ya = Rune("amumu")
    print(ya.rune_champ())
