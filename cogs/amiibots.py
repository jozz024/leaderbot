from nextcord.ext.commands import Context
import difflib
import asyncio
import re
from nextcord.ext import commands
import traceback
from nextcord import slash_command
from dictionaries import *
from nextcord import Interaction, SlashOption
import requests
import json
import os
import sys

skillsheet = requests.get(f"https://www.amiibots.com/api/spirit_skill").json()['data']
with open('spirits.json', 'w+') as skill:
    skill.write(json.dumps(skillsheet))
class amiibotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.async_call_shell = self.async_call_shell

    def restart_bot(self): 
        os.execv(sys.executable, ['py'] + sys.argv)

    def getskills(self, skill_id):
         with open('spirits.json', 'r') as skill:
            skillss = json.load(skill)
            for skills in skillss:
                if skills['id'] == skill_id:
                    return skills['name']
    async def async_call_shell(
        self, shell_command: str, inc_stdout=True, inc_stderr=True
    ):
        pipe = asyncio.subprocess.PIPE
        proc = await asyncio.create_subprocess_shell(
            str(shell_command), stdout=pipe, stderr=pipe
        )

        if not (inc_stdout or inc_stderr):
            return "??? you set both stdout and stderr to False????"

        proc_result = await proc.communicate()
        stdout_str = proc_result[0].decode("utf-8").strip()
        stderr_str = proc_result[1].decode("utf-8").strip()

        if inc_stdout and not inc_stderr:
            return stdout_str
        elif inc_stderr and not inc_stdout:
            return stderr_str

        if stdout_str and stderr_str:
            return f"stdout:\n\n{stdout_str}\n\n" f"======\n\nstderr:\n\n{stderr_str}"
        elif stdout_str:
            return f"stdout:\n\n{stdout_str}"
        elif stderr_str:
            return f"stderr:\n\n{stderr_str}"

        return "No output."

    def char(self, topbot, ruleset, character_name):
        try:
            if character_name == 'overall':
                character = None
            else:
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
        if character == None:
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
            characterlink = list(reversed(characterlink))
        printed_amiibo_count = 0
        for amiibo in characterlink:
            if amiibo["total_matches"] >= 30 and amiibo["is_banned"] == False:
                printed_amiibo_count += 1
                if amiibo['ruleset_id'] == '328d8932-456f-4219-9fa4-c4bafdb55776':
                    output += f"\n{printed_amiibo_count:>2}.) {amiibo['name']:^10} | {amiibo['attack_stat']}/{amiibo['defense_stat']} | {round(amiibo['rating'], 2):0^5} | {int(amiibo['wins'])}-{int(amiibo['losses'])}"
                    for spirits in amiibo['spirit_skill_ids']:
                        output += f"\n    -{self.getskills(spirits)}"
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

    @commands.is_owner()
    @commands.command(name = 'restart')
    async def restart(self, ctx):
        self.restart_bot()
        
    @slash_command(
        name="bestamiibo",
        description="Gives you the name and rating of the best amiibo in both vanilla and spirits",
    )
    async def getfirstnfp(
        self,
        interaction: Interaction, 
        ruleset = SlashOption(name="ruleset", choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want the data for."),
    ):
        try:
            rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
        except KeyError:
            try:
                ruleset = TRANSLATION_TABLE_RULESET[ruleset.lower().replace(" ", "")]
                rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
            except KeyError:
                await interaction.response.send_message("Invalid ruleset.", ephemeral=True)
        characterlink = requests.get(
            f"https://www.amiibots.com/api/amiibo?per_page=10&ruleset_id={rulesetid}"
        )
        firstnfprating = characterlink.json()["data"][0]["rating"]
        firstnfpname = characterlink.json()["data"][0]["name"]
        await interaction.response.send_message(
            f"The highest rated {ruleset} amiibo is: \n 1.) {firstnfpname} [{round(firstnfprating, 2)}]", 
            ephemeral=True
        )

    @slash_command(
        name="topoverall"
    )
    async def gettopthreenfp(
        self,
        interaction: Interaction, 
        ruleset = SlashOption(name="ruleset",choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want data for."),
    ):
        await interaction.send('Please wait while the data is being gathered for you.', ephemeral=True)
        await interaction.edit_original_message(content = self.char("highest", ruleset, "overall"))

    @slash_command(
        name="botoverall"
    )
    async def getbotthreenfp(
        self,
        interaction: Interaction, 
        ruleset = SlashOption(name="ruleset", choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want the data for."),
    ):
        await interaction.send('Please wait while the data is being gathered for you.', ephemeral=True)
        await interaction.edit_original_message(content = self.char("lowest", ruleset, "overall"))

    @slash_command(name="topchar")
    async def gettopthreenfpcharacter(
        self,
        interaction: Interaction, 
        character = SlashOption(name="character", description = "Character Name you want the data for."),
        ruleset = SlashOption(name="ruleset", choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want data for."),
    ):
        await interaction.send('Please wait while the data is being gathered for you.', ephemeral=True)
        await interaction.edit_original_message(content = self.char("highest", ruleset, character))

    @slash_command(name="botchar")
    async def getbotthreenfpcharacter(
        self,
        interaction: Interaction, 
        character = SlashOption(name="character", description = "Character Name you want the data for."),
        ruleset = SlashOption(name="ruleset", choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want the data for."),
):
        await interaction.send('Please wait while the data is being gathered for you.', ephemeral=True)
        await interaction.edit_original_message(content = self.char("lowest", ruleset, character))

    @slash_command(name="active")
    async def activechar( 
        self,
        interaction: Interaction, 
        character_name = SlashOption(name="character", description = "Character Name you want the data for."),
        ruleset = SlashOption(name="ruleset", choices={'vanilla':'vanilla','spirits':'spirits'}, description = "Ruleset you want the data for."),
    ):
        await interaction.send('Please wait while the data is being gathered for you.', ephemeral=True)
        try:
            if character_name == 'overall':
                character = None
            else:
                character = CHARACTER_NAME_TO_ID_MAPPING[character_name.lower()]
        except KeyError:
            try:
                character_name = TRANSLATION_TABLE_CHARACTER[
                    character_name.lower().replace(" ", "")
                ]
                character = CHARACTER_NAME_TO_ID_MAPPING[character_name]
            except KeyError:
                await interaction.send(f"'{character_name}' is an invalid character.", ephemeral=True)
        rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
        if character == None:
            characterlink = list(
                requests.get(
                    f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}"
                ).json()["data"]
            )
        else:
            characterlink = list(
                    requests.get(
                        f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}&playable_character_id={character}"
                    ).json()["data"]
            )
        amiiboactive = 0
        for amiibo in characterlink:
            if amiibo["is_active"] == True:
                amiiboactive = amiiboactive + 1
        if character != None:
            await interaction.edit_original_message(content = f"There are currently {amiiboactive} {character_name.title()} amiibo active in {ruleset}.")
        else: 
            await interaction.edit_original_message(content = f"There are currently {amiiboactive} amiibo active in {ruleset}.")
    @commands.is_owner()
    @commands.command()
    async def pull(self, ctx: Context, auto=False):
        """Does a git pull, bot manager only."""
        tmp = await ctx.send("Pulling...")
        git_output = await self.bot.async_call_shell("git pull")
        await tmp.edit(content=f"Pull complete. Output: ```{git_output}```")
        if auto:
            cogs_to_reload = re.findall(r"cogs/([a-z_]*).py[ ]*\|", git_output)
            for cog in cogs_to_reload:
                cog_name = "cogs." + cog
                try:
                    self.bot.unload_extension(cog_name)
                    self.bot.load_extension(cog_name)
                    await ctx.send(f":white_check_mark: `{cog}` successfully reloaded.")
                except:
                    await ctx.send(
                        f":x: Cog reloading failed, traceback: "
                        f"```\n{traceback.format_exc()}\n```"
                    )
                    return
    @gettopthreenfpcharacter.on_autocomplete("character")
    async def autocompletechar(self, interaction: Interaction, character):
        test = difflib.get_close_matches(character, CHARACTERS, 10, 0.3)
        try:
            if character == test[0]:
              test = [character]
        except IndexError:
            pass
        await interaction.response.send_autocomplete(test)

    @getbotthreenfpcharacter.on_autocomplete("character")
    async def autocompletechar(self, interaction: Interaction, character):
        test = difflib.get_close_matches(character, CHARACTERS, 10, 0.3)
        try:
            if character == test[0]:
              test = [character]
        except IndexError:
            pass
        await interaction.response.send_autocomplete(test)

    @activechar.on_autocomplete("character_name")
    async def autocompletechar(self, interaction: Interaction, character):
        test = difflib.get_close_matches(character, CHARACTERS, 10, 0.3)
        try:
            if character == test[0]:
              test = [character]
        except IndexError:
            pass
        await interaction.response.send_autocomplete(test)

def setup(bot):
    bot.add_cog(amiibotsCog(bot))
