import requests
import csv
import os
import time
from dictionaries import *
from datetime import date

amiibos = []
ruleset = input("Ruleset:\n").lower()
try:
    rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
except KeyError:
    ruleset = TRANSLATION_TABLE_RULESET[ruleset]
    rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
startTime = time.time()
characterlink = requests.get(
    f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}"
)
today = date.today()


for amiibo in characterlink.json()["data"]:
    id_to_char = {value: key for (key, value) in CHARACTER_NAME_TO_ID_MAPPING.items()}
    amiibogames = []
    amiibogames.insert(0, amiibo["name"])
    amiibogames.insert(1, id_to_char[amiibo["playable_character_id"]].title())
    amiibogames.insert(2, amiibo["rating"])
    amiibogames.insert(3, amiibo["win_percentage"])
    amiibogames.insert(4, amiibo["total_matches"])
    amiibogames.insert(5, amiibo["wins"])
    amiibogames.insert(6, amiibo["losses"])
    amiibogames.insert(7, amiibo["rating_mu"])
    amiibogames.insert(8, amiibo["rating_sigma"])
    amiibos.append(amiibogames)
amiibos.insert(
    0,
    [
        "name",
        "character_name",
        "rating",
        "win_percentage",
        "total_matches",
        "wins",
        "losses",
        "rating_mu",
        "rating_sigma",
    ],
)
with open(
    f'{ruleset.title()} Amiibots Rankings {today.strftime("%Y-%m-%d")}.csv',
    "w",
    newline="",
    encoding="utf-8",
) as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(amiibos)
print(
    f"Done! Gathered all of the {ruleset.title()} amiibots data in {round(time.time() - startTime, 2)} seconds!"
)
