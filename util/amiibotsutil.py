from dictionaries import CHARACTER_NAME_TO_ID_MAPPING, RULSET_NAME_TO_ID_MAPPING
import json
import requests

skillsheet = requests.get(f"https://www.amiibots.com/api/spirit_skill").json()['data']

with open('spirits.json', 'w+') as skill:
    skill.write(json.dumps(skillsheet))

base_url = 'https://www.amiibots.com/api/amiibo'

def validatechar(character):
            if character == 'overall':
                character = 'None'
            else:
                character = CHARACTER_NAME_TO_ID_MAPPING[character.lower()]
            return character

def getruleset(ruleset):
    ruleset = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
    return ruleset

def geturl(topbot, char_id, ruleset_id):
        if topbot == 'highest' and char_id == 'None':
            url = base_url + '?per_page=15&ruleset_id=' + ruleset_id
        elif topbot == 'lowest' and char_id == 'None':
            url = base_url + '?cursor=7&per_page=15&ruleset_id=' + ruleset_id
        elif topbot == 'highest' and char_id != 'None':
            url = base_url + '?per_page=30&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        elif topbot == 'lowest' and char_id != 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        elif topbot == 'active' and char_id == 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id
        elif topbot == 'active' and char_id != 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        return url

def getoutput(characterlink, output):
        printed_amiibo_count = 0
        for amiibo in characterlink:
            if amiibo["total_matches"] >= 30:
                printed_amiibo_count += 1
                if amiibo['ruleset_id'] == '328d8932-456f-4219-9fa4-c4bafdb55776':
                    output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {amiibo['attack_stat']}/{amiibo['defense_stat']} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"
                    for spirits in amiibo['spirit_skill_ids']:
                        output += f"\n    -{getskills(spirits)}"
                    output += '\n-----------------------------'
                else:
                    output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"

            if printed_amiibo_count >= 10:
                break
        output = output.strip('\n-----------------------------')
        output += "```"
        if printed_amiibo_count == 0:
            output = "No 30+ game amiibo for this character"
        return output

def getskills(skill_id):
         with open('spirits.json', 'r') as skill:
            skillss = json.load(skill)
            for skills in skillss:
                if skills['id'] == skill_id:
                    return skills['name']

def getactiveamiibo(character, ruleset):
    character_id = validatechar(character)
    ruleset_id = getruleset(ruleset)
    url = geturl('active', character_id, ruleset_id)
    characterlink = requests.get(url).json()['data']
    amiiboactive = 0
    for amiibo in characterlink:
        if amiibo["is_active"] == True:
                amiiboactive = amiiboactive + 1
    if character != None:
            return f"There are currently {amiiboactive} {character.title()} amiibo active in {ruleset}."
    else: 
            return f"There are currently {amiiboactive} amiibo active in {ruleset}."