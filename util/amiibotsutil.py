from dictionaries import CHARACTER_NAME_TO_ID_MAPPING, RULSET_NAME_TO_ID_MAPPING
import json
import aiohttp
from nextcord import Embed
from nextcord.ext import menus

base_url = 'https://www.amiibots.com/api/amiibo'

class MyEmbedFieldPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        embed = Embed(title=entries[6])
        embed.set_image(url = entries[5])
        embed.set_author(name = entries[4])
        res = any(map(lambda ele: ele is None, entries))
        if res == False:
            spirit_list = []
            for spirits in entries[7]:
                spirit_list.append(self.getskills(spirits))
            formatted_spirits = "    " + str(spirit_list).strip('[').strip(']').replace(',', '\n    ').replace("'", "")
            embed.add_field(name=entries[0], value=f"Rating: {entries[1]}\n\nRating MU: {entries[10]}\n\nWins: {entries[2]}\n\nLosses: {entries[3]}\n\nAttack: {entries[8]}\n\nDefense: {entries[9]}\n\nSkills: \n\n{formatted_spirits}", inline=True)
        else:
            embed.add_field(name=entries[0], value=f"Rating: {entries[1]}\n\nRating MU: {entries[10]}\n\nWins: {entries[2]}\n\nLosses: {entries[3]}", inline=True)

        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed

    def getskills(self, skill_id):
         with open('spirits.json', 'r') as skill:
            skillss = json.load(skill)
            for skills in skillss:
                if skills['id'] == skill_id:
                    return skills['name']
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
        # bad impl, but it has to stay until someone implements reverse sorting for the api
        if topbot == 'highest' and char_id == 'None':
            url = base_url + '?per_page=15&ruleset_id=' + ruleset_id
        elif topbot == 'lowest' and char_id == 'None':
            url = base_url + '?cursor=9&per_page=100&ruleset_id=' + ruleset_id
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
        # asyncly get the amiibots data
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return list((await resp.json())["data"])

    async def getoutput(self, amiibo_dict, output, detailed):
        printed_amiibo_count = 0
        # initializes the list of amiibo
        data = []
        # iterates through the dict of amiibo passed in
        for amiibo in amiibo_dict:
            # check if the amiibo is banned or if the user is banned
            if amiibo["user"]["is_banned"] is False and amiibo["is_banned"] is False:
                # sanitizes the name
                amiibo["name"] = await self.sanitize_text_for_discord(amiibo['name'])
                # check if detailed is true
                if detailed == "True":
                        # only do stuff if the amiibo's matches are greater than 30
                        if amiibo["total_matches"] >= 30:
                            # increase the number keeping track of the amount of amiibo added to the list
                            printed_amiibo_count += 1
                            # grab the character name and image from amiiboapi
                            image, character = await self.grab_img_and_char(amiibo["character_metadata"])
                            # check if ruleset is spirits and apply some spirits specific data if so
                            if amiibo["ruleset_id"] == RULSET_NAME_TO_ID_MAPPING["spirits: big 5 ban"] or amiibo["ruleset_id"] == RULSET_NAME_TO_ID_MAPPING["spirits: anything goes"]:
                                data.append((amiibo["name"], round(amiibo["rating"], 2), int(amiibo["wins"]), int(amiibo["losses"]), await self.getusername(amiibo['user']), image, character, amiibo['spirit_skill_ids'], amiibo["attack_stat"], amiibo["defense_stat"], round(amiibo["rating_mu"],2)))
                            # otherwise, leave all of those values none
                            else:
                                data.append((amiibo["name"], round(amiibo["rating"], 2), int(amiibo["wins"]), int(amiibo["losses"]), await self.getusername(amiibo['user']), image, character, None, None, None, round(amiibo["rating_mu"],2)))
                # for if detailed is false
                else:
                    # check if the amiibo's total matches are above 30
                    if amiibo["total_matches"] >= 30:
                        # increase the number that keeps track of the amount of times we've iterated
                        printed_amiibo_count += 1
                        # gen output
                        output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"
                        # add user
                        output += f"\n  Trainer: {await self.getusername(amiibo['user'])}"
                        # line of -- for easy reading
                        output += '\n-----------------------------'
                # break the loop if the amount of amiibo iterated through is 10
                if printed_amiibo_count >= 10:
                    break
            else:
                continue
        # make output a warning message if no 30 game amiibo exist
        if printed_amiibo_count == 0:
            output = "No 30+ game amiibo for this character"
        if detailed == "True":
            pages = menus.ButtonMenuPages(
                source=MyEmbedFieldPageSource(data),
                clear_buttons_after=True,
            )
            return pages
        else:
            # strip the line of -- since its the last line
            output = output.strip('\n-----------------------------')
            output += "```"
            return output

    def getskills(self, skill_id):
         with open('spirits.json', 'r') as skill:
            # load the skills and return the skill name if it matches the id
            skillss = json.load(skill)
            for skills in skillss:
                if skills['id'] == skill_id:
                    return skills['name']

    async def getactiveamiibo(self, character, ruleset):
        # get character id after validating the character
        character_id = self.validatechar(character)
        # get the ruleset from the ruleset string
        ruleset_id = self.getruleset(ruleset)
        # get the url
        url = self.geturl('active', character_id, ruleset_id)
        # get the amiibo dict from the url
        amiibo_dict = await self.get_amiibots_response(url)
        # the counter for how many of the amiibo are active (standby or active)
        amiiboactive = 0
        # iterate over the dict for the active amiibo
        for amiibo in amiibo_dict:
            if amiibo["match_selection_status"] != "INACTIVE":
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

    async def grab_img_and_char(self, id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://amiiboapi.com/api/amiibo/?id={id}") as resp:
                return (await resp.json())["amiibo"]["image"], (await resp.json())["amiibo"]["character"]