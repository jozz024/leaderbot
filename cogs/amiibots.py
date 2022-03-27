import difflib
from datetime import date

import aiohttp
import util.amiibotsutil
from dictionaries import CHARACTERS
from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext import commands


class amiibotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.amiibotsutil = util.amiibotsutil.utilities(bot)

    async def char(self, topbot, ruleset, character):
        character_id = self.amiibotsutil.validatechar(character)
        ruleset_id = self.amiibotsutil.getruleset(ruleset)
        url = self.amiibotsutil.geturl(topbot, character_id, ruleset_id)
        if character == "overall":
            output = f"The {topbot} rated {ruleset.title()} amiibo are:```"
        else:
            output = f"The {topbot} rated {ruleset.title()} {character.title()} are:```"
        characterlink = await self.amiibotsutil.get_amiibots_response(url)
        if topbot == "lowest":
            characterlink = list(reversed(characterlink))
        output = await self.amiibotsutil.getoutput(characterlink, output)
        return output

    @slash_command(name="topoverall")
    async def gettopthreenfp(
        self,
        interaction: Interaction,
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits": "spirits"},
            description="Ruleset you want data for.",
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )
        await interaction.edit_original_message(
            content=await self.char("highest", ruleset, "overall")
        )

    @slash_command(name="botoverall")
    async def getbotthreenfp(
        self,
        interaction: Interaction,
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits": "spirits"},
            description="Ruleset you want the data for.",
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )

        await interaction.edit_original_message(
            content=await self.char("lowest", ruleset, "overall")
        )

    @slash_command(name="topchar")
    async def gettopthreenfpcharacter(
        self,
        interaction: Interaction,
        character=SlashOption(
            name="character", description="Character Name you want the data for."
        ),
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits": "spirits"},
            description="Ruleset you want data for.",
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )
        await interaction.edit_original_message(
            content=await self.char("highest", ruleset, character)
        )

    @slash_command(name="botchar")
    async def getbotthreenfpcharacter(
        self,
        interaction: Interaction,
        character=SlashOption(
            name="character", description="Character Name you want the data for."
        ),
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits": "spirits"},
            description="Ruleset you want the data for.",
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )
        await interaction.edit_original_message(
            content=await self.char("lowest", ruleset, character)
        )

    @slash_command(name="active")
    async def activechar(
        self,
        interaction: Interaction,
        character_name=SlashOption(
            name="character", description="Character Name you want the data for."
        ),
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits": "spirits"},
            description="Ruleset you want the data for.",
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )
        await interaction.edit_original_message(
            content=await self.amiibotsutil.getactiveamiibo(character_name, ruleset)
        )

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

#    @tasks.loop(hours = 24.0)
#    async def updatedict(self):
#        today = date.today()
#        for users in self.user_dict:
#            userinfo = requests.get(f'https://amiibots/api/user/by_user_id/{users[0]["id"]}').json()['data']
#            users[0]['twitch_username'] = userinfo['twitch_username']
#            users[0]['discord_id'] = userinfo['discord_id']
#            users[1] = today.strftime("%Y-%m-%d")
def setup(bot):
    bot.add_cog(amiibotsCog(bot))
