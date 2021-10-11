import requests
import csv
import os
from dictionaries import *
print(os.getcwd())

amiibos = []
characterlink = requests.get("https://www.amiibots.com/api/amiibo?per_page=99999")

output = ''
printed_amiibo_count = 0
for amiibo in characterlink.json()["data"]:
    id_to_char = {value : key for (key, value) in CHARACTER_NAME_TO_ID_MAPPING.items()}
    amiibogames = list()
    amiibogames.insert(0, amiibo['name'])
    amiibogames.insert(1, id_to_char[amiibo["playable_character_id"]])
    amiibogames.insert(2, amiibo['rating'])
    amiibogames.insert(3, amiibo['win_percentage'])
    amiibogames.insert(4, amiibo['total_matches'])
    amiibogames.insert(5, amiibo['wins'])
    amiibogames.insert(6, amiibo['losses'])
    amiibogames.insert(7, amiibo['rating_mu'])
    amiibogames.insert(8, amiibo['rating_sigma'])
    amiibos.append(amiibogames)
amiibos.insert(0, ["name", "character_name", "rating", "win_percentage", "total_matches", "wins", "losses", "rating_mu", "rating_sigma"])
print(characterlink.json()["data"])
with open('newthing.csv', 'w', newline='', encoding="utf-8") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(amiibos)