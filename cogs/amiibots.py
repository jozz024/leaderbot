from nextcord.ext import commands
import nextcord
from dictionaries import *
import requests


class amiibotsCog(commands.Cog):
    def char(self, topbot, ruleset, character_name):
        try:
            character = CHARACTER_NAME_TO_ID_MAPPING[character_name.lower()]
        except KeyError:
            try:
                character_name = TRANSLATION_TABLE_CHARACTER[
                    character_name.lower().replace(" ", "")
                ]
                character = CHARACTER_NAME_TO_ID_MAPPING[character_name]
            except KeyError:
                return f"'{character_name}' is an invalid character."
        try:
            rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
        except KeyError:
            try:
                ruleset = TRANSLATION_TABLE_RULESET[ruleset.lower().replace(" ", "")]
                rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
            except KeyError:
                return f"'{ruleset}' is an invalid ruleset."
        if character_name.lower() == "overall":
            characterlink = list(
                requests.get(
                    f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}"
                ).json()["data"]
            )
            output = f"The {topbot} rated {ruleset.title()} amiibo are:```"
        else:
            characterlink = list(
                requests.get(
                    f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}&playable_character_id={character}"
                ).json()["data"]
            )
            output = (
                f"The {topbot} rated {ruleset.title()} {character_name.title()} are:```"
            )
        if topbot == "lowest":
            characterlink.reverse()
        printed_amiibo_count = 0
        for amiibo in characterlink:
            if amiibo["total_matches"] >= 30 and amiibo["is_banned"] == False:
                printed_amiibo_count += 1
                amiibo_win_percent = float(amiibo["win_percentage"]) * 100
                output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"
            if printed_amiibo_count >= 10:
                break
        output += "```"
        if printed_amiibo_count == 0:
            output = "No 30+ game amiibo for this character"
        return output

    @commands.command(
        name="bestamiibo",
        description="Gives you the name and rating of the best amiibo in both vanilla and spirits",
    )
    async def getfirstnfp(self, ctx, ruleset):
        try:
            rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
        except KeyError:
            try:
                ruleset = TRANSLATION_TABLE_RULESET[ruleset.lower().replace(" ", "")]
                rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
            except KeyError:
                ctx.send("Invalid ruleset.")
        characterlink = requests.get(
            f"https://www.amiibots.com/api/amiibo?per_page=10&ruleset_id={rulesetid}"
        )
        firstnfprating = characterlink.json()["data"][0]["rating"]
        firstnfpname = characterlink.json()["data"][0]["name"]
        await ctx.send(
            f"The highest rated {ruleset} amiibo is: \n 1.) {firstnfpname} [{round(firstnfprating, 2)}]"
        )

    @commands.command(
        name="topoverall",
        description="Gives you the top 10 overall amiibo in both vanilla and spirits.",
    )
    async def gettopthreenfp(self, ctx, ruleset):
        await ctx.send(self.char("highest", ruleset, "overall"))

    @commands.command(
        name="botoverall",
        description="Gives you the top 10 overall amiibo in both vanilla and spirits.",
    )
    async def getbotthreenfp(self, ctx, ruleset):
        await ctx.send(self.char("lowest", ruleset, "overall"))

    @commands.command(name="topchar")
    async def gettopthreenfpcharacter(self, ctx, ruleset, *, character_name):
        await ctx.send(self.char("highest", ruleset, character_name))

    @commands.command(name="botchar")
    async def getbotthreenfpcharacter(self, ctx, ruleset, *, character_name):
        await ctx.send(self.char("lowest", ruleset, character_name))


def setup(bot):
    bot.add_cog(amiibotsCog(bot))
