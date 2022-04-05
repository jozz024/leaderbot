from dictionaries import CHARACTER_NAME_TO_ID_MAPPING, RULSET_NAME_TO_ID_MAPPING
import json
import aiohttp

base_url = 'https://www.amiibots.com/api/amiibo'

class utilities():
    def __init__(self, bot):
        self.bot = bot

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
            url = base_url + '?cursor=8&per_page=100&ruleset_id=' + ruleset_id
        elif topbot == 'highest' and char_id != 'None':
            url = base_url + '?per_page=30&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        elif topbot == 'lowest' and char_id != 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        elif topbot == 'active' and char_id == 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id
        elif topbot == 'active' and char_id != 'None':
            url = base_url + '?per_page=99999&ruleset_id=' + ruleset_id + '&playable_character_id=' + char_id
        return url

    async def get_amiibots_response(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return list((await resp.json())["data"])

    async def getoutput(self, characterlink, output):
        printed_amiibo_count = 0
        for amiibo in characterlink:
            if amiibo["user"]["is_banned"] is False and amiibo["is_banned"] is False:
                amiibo["name"] = await self.sanitize_text_for_discord(amiibo['name'])
                if amiibo["total_matches"] >= 30:
                    printed_amiibo_count += 1

                    if amiibo['ruleset_id'] == '328d8932-456f-4219-9fa4-c4bafdb55776':
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {amiibo['attack_stat']}/{amiibo['defense_stat']} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"

                        output += f"\n  Trainer: {await self.getusername(amiibo['user'])}"

                        for spirits in amiibo['spirit_skill_ids']:
                            output += f"\n    -{self.getskills(spirits)}"
                        output += '\n-----------------------------'
                    else:
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"
                        output += f"\n  Trainer: {await self.getusername(amiibo['user'])}"
                        output += '\n-----------------------------'
                if printed_amiibo_count >= 10:
                    break
            else:
                continue
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

    async def getactiveamiibo(self, character, ruleset):
        character_id = self.validatechar(character)
        ruleset_id = self.getruleset(ruleset)
        url = self.geturl('active', character_id, ruleset_id)
        characterlink = await self.get_amiibots_response(url)
        amiiboactive = 0
        for amiibo in characterlink:
            if amiibo["is_active"] == True:
                amiiboactive = amiiboactive + 1
        if character != None:
            return f"There are currently {amiiboactive} {character.title()} amiibo active in {ruleset}."
        else:
            return f"There are currently {amiiboactive} amiibo active in {ruleset}."

    async def getusername(self, userinfo):
        if userinfo["discord_id"] is None:
            return userinfo["twitch_user_name"]
        else:
            return await self.get_discord_username(int(userinfo["discord_id"]))

    async def get_discord_username(self, userid):
            user = await self.bot.fetch_user(userid)
            return user.name

    async def sanitize_text_for_discord(self, text: str):
        return text.replace("`", "'")