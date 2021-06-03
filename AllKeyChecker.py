import sys
import requests
from bs4 import BeautifulSoup


def get_gamelink():
    gamename = sys.argv
    gamename.pop(0)
    return "https://www.allkeyshop.com/blog/catalogue/search-" + "+".join(gamename)


def get_gamelist(games):
    arr = []
    for game in games:
        link = game.get("href")
        name = game.find("h2", recursive="false").string
        price = game.find(
            "div", {"class": "search-results-row-price"}, recursive="false").text.strip()
        arr.append({"link": link, "name": name, "price": price})
    return arr


r = requests.get(get_gamelink())
soup = BeautifulSoup(r.text, "html.parser")
games = soup.find_all('a', {"class": "search-results-row-link"})
gamelist = get_gamelist(games)

print()
if gamelist:
    for i, val in enumerate(gamelist):
        print(f"{i+1}. {val['name']} - {val['price']}")
else:
    print("Didn't found any listings for that game")
