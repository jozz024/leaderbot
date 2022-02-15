from dictionaries import CHARACTER_NAME_TO_ID_MAPPING, RULSET_NAME_TO_ID_MAPPING
import json
import requests
import datetime 
from datetime import date
skillsheet = requests.get(f"https://www.amiibots.com/api/spirit_skill").json()['data']

with open('spirits.json', 'w+') as skill:
    skill.write(json.dumps(skillsheet))

base_url = 'https://www.amiibots.com/api/amiibo'

class utilities():
    def __init__(self):
        # The user dictionary for the upcoming api user feature
        self.user_dict = {
#            "0369ba61-e623-47e6-b13d-a13d6dcb8dd9": [
#                {
 #                   "id": "0369ba61-e623-47e6-b13d-a13d6dcb8dd9",
 #                   "twitch_username": "jozz024",
 #                   "discord_id": '554854714794049537',
 #               },
 #               "2022-2-5",
  #          ]
        }
    def validatechar(self, character):
            #makes the character id none for later use
            if character == 'overall':
                character = 'None'
            else:
                #if character isnt none, map character name to the character id
                character = CHARACTER_NAME_TO_ID_MAPPING[character.lower()]
            #returns the character id
            return character

    def getruleset(self, ruleset):
        #maps the ruleset name to id
        ruleset = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
        return ruleset

    def geturl(self, topbot, char_id, ruleset_id):
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

    async def getoutput(self, characterlink, output, bot):
        printed_amiibo_count = 0
        for amiibo in characterlink:
            if amiibo["total_matches"] >= 30:
                printed_amiibo_count += 1

                if amiibo['ruleset_id'] == '328d8932-456f-4219-9fa4-c4bafdb55776':
                    if self.user_dict.get(amiibo['user']) != None:
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {amiibo['attack_stat']}/{amiibo['defense_stat']} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])} | {await self.getusername(amiibo['user'], bot)}"
                    else:
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {amiibo['attack_stat']}/{amiibo['defense_stat']} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"

                    for spirits in amiibo['spirit_skill_ids']:
                        output += f"\n    -{self.getskills(spirits)}"
                    output += '\n-----------------------------'
                else:
                    if self.user_dict.get(amiibo['user']) != None:
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])} | {await self.getusername(amiibo['user'], bot)}"
                    else:
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"

            if printed_amiibo_count >= 10:
                break
        output = output.strip('\n-----------------------------')
        output += "```"
        if printed_amiibo_count == 0:
            output = "No 30+ game amiibo for this character"
        return output

    def getskills(self, skill_id):
         with open('spirits.json', 'r') as skill:
            skillss = json.load(skill)
            for skills in skillss:
                if skills['id'] == skill_id:
                    return skills['name']

    def getactiveamiibo(self, character, ruleset):
        character_id = self.validatechar(character)
        ruleset_id = self.getruleset(ruleset)
        url = self.geturl('active', character_id, ruleset_id)
        characterlink = requests.get(url).json()['data']
        amiiboactive = 0
        for amiibo in characterlink:
            if amiibo["is_active"] == True:
                amiiboactive = amiiboactive + 1
        if character != None:
            return f"There are currently {amiiboactive} {character.title()} amiibo active in {ruleset}."
        else: 
            return f"There are currently {amiiboactive} amiibo active in {ruleset}."
            
    def getUserById(self, user_id):
        iso_time_str = datetime.datetime.fromisoformat(self.user_dict[user_id][1])
        user_not_in_cache_or_outdated = user_id not in self.user_dict or (datetime.datetime.now() - iso_time_str) >= datetime.timedelta(hours=24)
        if user_not_in_cache_or_outdated:
            userinfo = requests.get(f'https://amiibots/api/user/by_user_id/{user_id}').json()
            self.user_dict[user_id] = [userinfo, datetime.datetime.now().isoformat()]
        else:
            userinfo = self.user_dict[user_id]
        return userinfo

    async def getusername(self, user_id, bot):
        iso_time_str = datetime.datetime.fromisoformat(self.user_dict[user_id][1])
        user_not_in_cache_or_outdated = user_id not in self.user_dict or (datetime.datetime.now() - iso_time_str) >= datetime.timedelta(hours=24)
        if not user_not_in_cache_or_outdated:
            userinfo = self.user_dict[user_id]
        else:
        #    userinfo = requests.get(f'https://amiibots/api/user/by_user_id/{user_id}').json()
        #    self.user_dict[user_id] = [userinfo, datetime.datetime.now().isoformat()]
            userinfo = self.user_dict[user_id]

        if userinfo[0]['discord_id'] != None:
            user = await bot.fetch_user(int(userinfo[0]['discord_id']))
            return user.name
        else:
            return userinfo[0]['twitch_username']