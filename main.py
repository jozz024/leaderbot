import requests
import nextcord
import asyncio
from nextcord.ext import commands
import os
import re
from nextcord import File
from character_dictionary import CharacterDictionary
from amiibo_functions import BinManager
from amiibo import AmiiboMasterKey
from ssbu_amiibo import SsbuAmiiboDump as AmiiboDump
from dictionaries import *


TOKEN = os.environ["token"]
bot = commands.Bot(command_prefix="!", description="deez")
default_assets_location = r"Brain_Transplant_Assets"
characters_location = r"Brain_Transplant_Assets/characters.xml"
char_dict = CharacterDictionary(characters_location)
binmanagerinit = BinManager(char_dict)
STORAGE_DIR = "./amiibo/"


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await bot.change_presence(
        status=nextcord.Status.idle,
        activity=nextcord.Activity(name="amiibots", type=nextcord.ActivityType.listening),
    )



@bot.command(name="bestamiibo", description="Gives you the name and rating of the best amiibo in both vanilla and spirits")
async def getfirstnfp(ctx, ruleset):
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


@bot.command(name="topoverall", description="Gives you the top 10 overall amiibo in both vanilla and spirits.")
async def gettopthreenfp(ctx, ruleset):
    try:
        rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
    except KeyError:
        try:
            ruleset = TRANSLATION_TABLE_RULESET[ruleset.lower().replace(" ", "")]
            rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
        except KeyError:
            await ctx.send(f"'{ruleset}' is an invalid ruleset.")

    characterlink = requests.get(
        f"https://www.amiibots.com/api/amiibo?per_page=10&ruleset_id={rulesetid}"
    )

    output = f"The highest rated {ruleset.title()} amiibo are:"

    for i in range(0, 10):
        try:
            output += f"\n {i + 1}.) {characterlink.json()['data'][i]['name']} [{round(characterlink.json()['data'][i]['rating'], 2)}]"
        except IndexError:
            output += f"\n {i + 1}.) No more amiibo"

    await ctx.send(output)


@bot.command(name="topchar")
async def gettopthreenfpcharacter(ctx, ruleset, *, character_name):
    try:
        character = CHARACTER_NAME_TO_ID_MAPPING[character_name.lower()]
    except KeyError:
        try:
            character_name = TRANSLATION_TABLE_CHARACTER[
                character_name.lower().replace(" ", "")
            ]
            character = CHARACTER_NAME_TO_ID_MAPPING[character_name]
        except KeyError:
            await ctx.send(f"'{character_name}' is an invalid character.")
    try:
        rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset.lower()]
    except KeyError:
        try:
            ruleset = TRANSLATION_TABLE_RULESET[ruleset.lower().replace(" ", "")]
            rulesetid = RULSET_NAME_TO_ID_MAPPING[ruleset]
        except KeyError:
            await ctx.send(f"'{ruleset}' is an invalid ruleset.")

    characterlink = requests.get(
        f"https://www.amiibots.com/api/amiibo?per_page=99999&ruleset_id={rulesetid}&playable_character_id={character}"
    )

    output = f"The highest rated {ruleset.title()} {character_name.title()} are:"

    printed_amiibo_count = 0
    for amiibo in characterlink.json()["data"]:
        if amiibo["total_matches"] >= 30:
            printed_amiibo_count += 1
            output += f"\n {printed_amiibo_count}.) {amiibo['name']} [{round(amiibo['rating'], 2)}]"
        if printed_amiibo_count >= 10:
            break
    if printed_amiibo_count == 0:
        output = "No 30+ game amiibo for this character"
    await ctx.send(output)


@bot.command(name="convert")
@commands.dm_only()
async def convert_nfc_tools_file_to_bin(ctx):
    export_string_lines = None
    hex = ""
    print(str(ctx.message.attachments[0].filename))
    # if 'url' in str(message.attachments):
    # print(str(message.attachments.url))
    await ctx.message.attachments[0].save(fp="txt files/nextcord.txt")
    with open("txt files/nextcord.txt") as file:
        export_string_lines = file.readlines()

    for line in export_string_lines:
        match = re.search(r"(?:[A-Fa-f0-9]{2}:){3}[A-Fa-f0-9]{2}", line)
        if match:
            hex = hex + match.group(0).replace(":", "")

    bin = bytes.fromhex(hex)
    with open(
        f"bin files/{str(ctx.message.attachments[0].filename).strip('.txt')}.bin",
        mode="wb",
    ) as new_file:
        new_file.write(bin)
    await ctx.send(
        file=File(
            f"bin files/{str(ctx.message.attachments[0].filename).strip('.txt')}.bin"
        )
    )


@bot.command(name="transplant")
@commands.dm_only()
async def brain_transplant(ctx, *, character):
    try:
        character = character
        await ctx.message.attachments[0].save(
            fp=f"old bins/{ctx.message.attachments[0].filename}"
        )
        binmanagerinit.transplant(
            bin_location=f"old bins/{ctx.message.attachments[0].filename}",
            character=character.title(),
            saveAs_location=f"new bins/{ctx.message.attachments[0].filename}",
            randomize_SN=True,
        )
        await ctx.send(file=File(f"new bins/{ctx.message.attachments[0].filename}"))
    except KeyError:
        try:
            character = TRANSLATION_TABLE_CHARACTER_TRANSPLANT[
                character.replace(" ", "")
            ]
            await ctx.message.attachments[0].save(
                fp=f"old bins/{ctx.message.attachments[0].filename}"
            )
            binmanagerinit.transplant(
                bin_location=f"old bins/{ctx.message.attachments[0].filename}",
                character=character.title(),
                saveAs_location=f"new bins/{ctx.message.attachments[0].filename}",
                randomize_SN=True,
            )
            await ctx.send(file=File(f"new bins/{ctx.message.attachments[0].filename}"))
        except KeyError:
            await ctx.send(f"'{character}' is an invalid character.")


@bot.command(name="shuffleSN".lower())
@commands.dm_only()
async def shufflenfpsn(ctx):
    await ctx.message.attachments[0].save(
        fp=f"old bins/{ctx.message.attachments[0].filename}"
    )
    binmanagerinit.randomize_sn(
        bin_location=f"old bins/{ctx.message.attachments[0].filename}"
    )
    await ctx.send(file=File(f"old bins/{ctx.message.attachments[0].filename}"))


@bot.command(name="setspirits")
@commands.dm_only()
async def spiritedit(ctx, attack, defense, ability1 = 'none', ability2 = 'none', ability3 = 'none'):
    await ctx.message.attachments[0].save(
        fp=f"old bins/{ctx.message.attachments[0].filename}"
    )
    print(ability1)
    print(ability2)
    print(ability3)
    try:
        binmanagerinit.setspirits(
            f"old bins/{ctx.message.attachments[0].filename}",
            attack,
            defense,
            ability1,
            ability2,
            ability3,
            f"new bins/{ctx.message.attachments[0].filename}",
        )
        await ctx.send(
            f"{attack}, {defense}",
            file=File(f"new bins/{ctx.message.attachments[0].filename}"),
        )
    except IndexError:
        await ctx.send("Illegal Setup")


@bot.command(name="rename")
@commands.dm_only()
async def rename(ctx, *, newamiiboname):
    await ctx.message.attachments[0].save(
        fp=f"old bins/{ctx.message.attachments[0].filename}"
    )
    with open(r"/".join([default_assets_location, "key_retail.bin"]), "rb") as fp_j:
        master_keys = AmiiboMasterKey.from_combined_bin(fp_j.read())
    with open(f"old bins/{ctx.message.attachments[0].filename}", "rb") as fp:
        dump = AmiiboDump(master_keys, fp.read())
    dump.unlock()
    dump.amiibo_nickname = newamiiboname
    dump.lock()
    with open(f"new bins/{ctx.message.attachments[0].filename}", "wb") as fp:
        fp.write(dump.data)
    await ctx.send(file=File(f"new bins/{ctx.message.attachments[0].filename}"))


@bot.command(name="list")
async def list(ctx):
    await ctx.send(
        str(TRANSLATION_TABLE_CHARACTER)
        .replace(":", " -->")
        .replace(",", "\n")
        .strip("{")
        .strip("}")
        .replace("'", "")
    )


@bot.command(name="decrypt")
@commands.is_owner()
async def decrypt(ctx):
    await ctx.message.attachments[0].save(
        fp=f"old bins/{ctx.message.attachments[0].filename}"
    )
    binmanagerinit.decrypt(
        f"old bins/{ctx.message.attachments[0].filename}",
        f"new bins/{ctx.message.attachments[0].filename}",
    )
    await ctx.send(file=File(f"new bins/{ctx.message.attachments[0].filename}"))


@bot.command(name="binedit")
@commands.is_owner()
async def binedit(ctx, aggression, edgeguard, anticipation, defensiveness):
    await ctx.message.attachments[0].save(
        fp=f"old bins/{ctx.message.attachments[0].filename}"
    )
    binmanagerinit.personalityedit(
        f"old bins/{ctx.message.attachments[0].filename}",
        aggression,
        edgeguard,
        anticipation,
        defensiveness,
        f"new bins/{ctx.message.attachments[0].filename}",
    )
    await ctx.send(file=File(f"new bins/{ctx.message.attachments[0].filename}"))

@bot.command(name="storagehelp")
async def help_cmd(ctx):
    retmsg = (
        "`!store <amiibo nickname>` (and attach the bin)\n"
        "`!listbins`\n"
        "`!renamestoredbin <old amiibo nickname>, <new amiibo nickname>`\n"
        "`!delete <amiibo nickname>`\n"
        # "`!send <Tag the host> <amiibo nickname>`\n"
        "`!download <amiibonickname>`"
    )
    await ctx.send(retmsg)


@bot.command(name="listbins")
async def list_cmd(ctx):
    filelist = os.listdir(STORAGE_DIR)
    amiibolist = [x for x in filelist if x.startswith(str(ctx.author.id))]
    namelist = ["-".join(x.split("-")[1:]).replace(".bin", "") for x in amiibolist]
    print(namelist)
    retmsg = "The amiibo you have stored are:\n" + "\n".join(namelist)
    await ctx.send(retmsg)


@bot.command(name="delete")
@commands.dm_only()
async def delete_cmd(ctx, to_del):
    try:
        filename = STORAGE_DIR + str(ctx.author.id) + "-" + to_del + ".bin"
        os.remove(filename)
        await ctx.send(f"Successfully deleted {to_del}")
    except Exception as exc:
        logging.warning(exc)
        await ctx.send("Deletion Failed")


@bot.command(name="renamestoredbin")
@commands.dm_only()
async def rename_cmd(ctx, oldname, newname):
    try:
        oldfilename = STORAGE_DIR + str(ctx.author.id) + "-" + oldname + ".bin"
        newfilename = STORAGE_DIR + str(ctx.author.id) + "-" + newname + ".bin"
        os.rename(oldfilename, newfilename)
        await ctx.send("Successfully renamed {} to {}".format(oldname, newname))
    except Exception as exc:
        if "No such file or directory" in str(exc):
            await ctx.send("File does not exist, make sure your spelling is correct")
        elif "not enough values to unpack" in str(exc):
            await ctx.send("Not enough names provided, should be comma separated")
        elif "too many values to unpack" in str(exc):
            await ctx.send("Too many names provided, calm down")
        else:
            await ctx.send("Failed to rename")


@bot.command(name="store")
@commands.dm_only()
async def store_cmd(ctx, nick):
    BINSIZES = [532, 540, 572]
    if ctx.message.attachments[0].size in BINSIZES and ctx.message.attachments[0].filename.endswith('bin'):
        try:
            filepathname = STORAGE_DIR + str(ctx.author.id) + "-" + nick + ".bin"
            await ctx.message.attachments[0].save(fp=filepathname)
            await ctx.send("Successfully stored - " + nick)
        except Exception as exc:
            logging.warning(exc)
            await ctx.send("Failed to Store")
    else:
        await ctx.send("Improper bin size")


@bot.command(name="send")
async def send(ctx, to_send):
    try:
            recipient = ctx.message.mentions[0]
            filename = STORAGE_DIR + str(ctx.author.id) + "-" + to_send + ".bin"
            sendname = STORAGE_DIR + to_send + ".bin"
            os.rename(filename, sendname)
            await ctx.send(file=File(sendname))
            os.rename(sendname, filename)
            await ctx.send(
                "Successfully sent {} to {}".format(to_send, str(recipient)),
            )
    except Exception as exc:
            logging.warning(exc)
            if "Cannot send messages to this user" in str(exc):
                await ctx.send(
                    "Cannot send messages to this user, they may have DMs turned off"
                )
            elif "No such file or directory" in str(exc):
                await ctx.send(
                    "File does not exist, make sure your spelling is correct"
                )
            else:
                await ctx.send("Failed to Send")


@bot.command(name="download")
@commands.dm_only()
async def dl(ctx, amiiname):
    try:
            filename = STORAGE_DIR + str(ctx.author.id) + "-" + amiiname + ".bin"
            sendname = STORAGE_DIR + amiiname + ".bin"
            os.rename(filename, sendname)
            await ctx.send(file=File(sendname))
            os.rename(sendname, filename)
    except Exception as exc:
            logging.warning(exc)
            if "No such file or directory" in str(exc):
                await ctx.send(
                    "File does not exist, make sure your spelling is correct"
                )
            else:
                await ctx.send("Failed to Download")

@bot.command(name="end")
async def end(ctx):
    exit()
    
    
@convert_nfc_tools_file_to_bin.error
async def convert_nfc_tools_file_to_bin_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")


@brain_transplant.error
async def brain_transplant_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")


@shufflenfpsn.error
async def shufflenfpsn_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")

@spiritedit.error
async def setspirits_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")

@delete_cmd.error
async def delete_cmd_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")
        
@rename_cmd.error
async def rename_cmd_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")

@store_cmd.error
async def store_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")
        
@dl.error
async def dl_err(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You are not in a DM")

loop = asyncio.get_event_loop()
loop.run_until_complete(
    bot.start(token)
)


        
