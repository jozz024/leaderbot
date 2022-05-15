import difflib
import util.amiibotsutil
from dictionaries import CHARACTERS
from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext import commands


class amiibotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # initialize it on cog load because we need the bot variable
        self.amiibotsutil = util.amiibotsutil.utilities(bot)

    async def char(self, topbot: str, ruleset: str, character: str, detailed: str):
        # get character id from the str
        character_id = self.amiibotsutil.validatechar(character)
        # get ruleset id from the str
        ruleset_id = self.amiibotsutil.getruleset(ruleset)
        # get url from character id, ruleset id, and top or bottom
        url = self.amiibotsutil.geturl(topbot, character_id, ruleset_id)
        # if character is overall, dont add character to the message
        if character == "overall":
            output = f"The {topbot} rated {ruleset.title()} amiibo are:```"
        # else, replace `amiibo` with the character
        else:
            output = f"The {topbot} rated {ruleset.title()} {character.title()} are:```"

        amiibo_dict = await self.amiibotsutil.get_amiibots_response(url)
        if topbot == "lowest":
            amiibo_dict = list(reversed(amiibo_dict))
        output = await self.amiibotsutil.getoutput(amiibo_dict, output, detailed)
        return output

    @slash_command(name="topoverall")
    async def gettopthreenfp(
        self,
        interaction: Interaction,
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits: big 5 ban": "spirits: big 5 ban", "spirits: anything goes": "spirits: anything goes"},
            description="Ruleset you want data for.",
        ),
        detailed=SlashOption(
            name="detailed", description="use detailed amiibo listing?", default = "False", choices={"True": "True", "False": "False"}, required=False
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )

        if detailed == "False":
            await interaction.edit_original_message(
                content=await self.char("highest", ruleset, "overall", detailed)
                )
        else:
            try:
                pages = await self.char("highest", ruleset, "overall", detailed)

                await pages.start(interaction=interaction, ephemeral = True)
            except AttributeError:
                await interaction.edit_original_message(
                content= "The new menus currently do not work in DMs, apologies.\n\n" + await self.char("highest", ruleset, "overall", "False")
                )

    @slash_command(name="botoverall")
    async def getbotthreenfp(
        self,
        interaction: Interaction,
        ruleset=SlashOption(
            name="ruleset",
            choices={"vanilla": "vanilla", "spirits: big 5 ban": "spirits: big 5 ban", "spirits: anything goes": "spirits: anything goes"},
            description="Ruleset you want data for.",
        ),
        detailed=SlashOption(
            name="detailed", description="use detailed amiibo listing?", default = "False", choices={"True": "True", "False": "False"}, required=False
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )

        if detailed == "False":
            await interaction.edit_original_message(
                content=await self.char("lowest", ruleset, "overall", detailed)
                )
        else:
            try:
                pages = await self.char("lowest", ruleset, "overall", detailed)

                await pages.start(interaction=interaction, ephemeral = True)
            except AttributeError:
                await interaction.edit_original_message(
                content= "The new menus currently do not work in DMs, apologies.\n\n" + await self.char("lowest", ruleset, "overall", "False")
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
            choices={"vanilla": "vanilla", "spirits: big 5 ban": "spirits: big 5 ban", "spirits: anything goes": "spirits: anything goes"},
            description="Ruleset you want data for.",
        ),
        detailed=SlashOption(
            name="detailed", description="use detailed amiibo listing?", default = "False", choices={"True": "True", "False": "False"}, required=False
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )

        if detailed == "False":
            await interaction.edit_original_message(
                content=await self.char("highest", ruleset, character, detailed)
                )
        else:
            try:
                pages = await self.char("highest", ruleset, character, detailed)

                await pages.start(interaction=interaction, ephemeral = True)
            except AttributeError:
                await interaction.edit_original_message(
                content= "The new menus currently do not work in DMs, apologies.\n\n" + await self.char("highest", ruleset, character, "False")
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
            choices={"vanilla": "vanilla", "spirits: big 5 ban": "spirits: big 5 ban", "spirits: anything goes": "spirits: anything goes"},
            description="Ruleset you want data for.",
        ),
        detailed=SlashOption(
            name="detailed", description="use detailed amiibo listing?", default = "False", choices={"True": "True", "False": "False"}, required=False
        ),
    ):
        await interaction.send(
            "Please wait while the data is being gathered for you.", ephemeral=True
        )

        if detailed == "False":
            await interaction.edit_original_message(
                content=await self.char("lowest", ruleset, character, detailed)
                )
        else:
            try:
                pages = await self.char("lowest", ruleset, character, detailed)

                await pages.start(interaction=interaction, ephemeral = True)
            except AttributeError:
                await interaction.edit_original_message(
                content= "The new menus currently do not work in DMs, apologies.\n\n" + await self.char("lowest", ruleset, character, "False")
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
            choices={"vanilla": "vanilla", "spirits: big 5 ban": "spirits: big 5 ban", "spirits: anything goes": "spirits: anything goes"},
            description="Ruleset you want data for.",
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
