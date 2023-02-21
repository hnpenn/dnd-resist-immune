import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

df = pd.read_csv('monster data.csv')
names = list(df['Creature '])
data = {
        "Creature" : [],
        "Immunities": [],
        "Resistances": []
        }
damage_types = ["acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic", "piercing", "poison", "psychic", "radiant", "slashing", "thunder"]
for d in damage_types:
    data.update({d: []})
for n in names:
    URL = "https://www.aidedd.org/dnd/monstres.php?vo={name}".format(name = re.sub("[^a-z1-9é-]", "", re.sub("(\s)|(')|\/", "-", n.lower())))
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find_all("div", class_="red")[0]
    im = re.findall(r"(?<=Damage Immunities<\/strong>)[a-z ,]+", str(text))
    res = re.findall(r"(?<=Damage Resistances<\/strong>)[a-z ,]+", str(text))
    for d in damage_types:
        if len(im) > 0 and d in im[0]:
            data[d].append(1)
        elif len(res) > 0 and d in res[0]:
            data[d].append(0.5)
        else:
            data[d].append(0)
    data["Creature"].append(n)
    data["Immunities"].append(im)
    data["Resistances"].append(res)

final_data = pd.DataFrame.from_dict(data)
df.to_csv("monsterri.csv")