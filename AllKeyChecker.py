import bs4
import requests
import os
import sys
import json
import rich
import msvcrt
from rich.console import Console
from rich.table import Table


def getGameInfo(x):
    a1 = x.a(class_="search-results-row-price")[0].text
    return {"name": x.a(class_="search-results-row-game-title")[0].text, "price": ' '.join(a1.split()), "link": x.a['href']}


def steamPrice(x):
    r = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    jsondata = json.loads(r.content)
    final = ""
    for x in jsondata['applist']['apps']:
        if x['name'].lower() == ft:
            final = x['appid']
            break
    if final == "":
        return "not listed"
    r = requests.get(
        f"https://store.steampowered.com/api/appdetails?appids={final}&cc=de")
    jsondata = json.loads(r.content)
    return jsondata[f'{final}']['data']['price_overview']['final_formatted']


console = Console()
table = Table(show_header=True, box=rich.box.MINIMAL)
table.add_column(header="#", min_width=1)
table.add_column(header="Title", header_style="Bold Red", style="Red")
table.add_column(
    header="Price", header_style="Bold Yellow", style="Yellow")
table.add_column(header="Link", no_wrap=True,
                 header_style="Bold Blue", style="Blue")

console.clear()
ft = input("game title: ").lower()
fft = ft.replace(" ", "+")

txt = requests.get(f"https://www.allkeyshop.com/blog/catalogue/search-{fft}/")

soup = bs4.BeautifulSoup(txt.content, 'html.parser')
found = soup.find_all("li", class_="search-results-row")

if len(found) == 0:
    console.print(
        "\n[bold red]There isn't any game listed under that name on AKS.[/bold red]")
    sys.exit()

max_entries = 5
if len(found) < 5:
    max_entries = 3
elif len(found) < 3:
    max_entries = 1

for x in range(0, max_entries):
    info = getGameInfo(found[x])
    table.add_row(str(x+1), info['name'], info['price'], info['link'])
    table.add_row()

secondmessage = f"[bold red]current steam price: [/bold red][yellow]{steamPrice(ft)}[/yellow]"
print()
console.print(table)
console.print(secondmessage)
console.print("\ncreated by:\nhttps://github.com/Natqo")
