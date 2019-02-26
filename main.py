import discord
from discord.ext import commands
import logging
import json

#prefs.json is used to store things like the command prefix and any channel ids that need to be saved between sessions
try:
    prefsDict = json.load(open("prefs.json"))
except Exception as ex:
    prefsDict = { "commandPrefix": "f!" }
    with open("prefs.json", "w") as outfile:
        json.dump(prefsDict, outfile)

#secrets.json is used to store any api keys or information that shouldn't be publicly available
try:
    secretsDict = json.load(open("secrets.json"))
    if (secretsDict["token"] == "REPLACE THIS WITH TOKEN"):
        print("Add your token to secrets.json")
        exit()
except Exception as ex:
    print(str(ex))
    secretsDict = { "token": "REPLACE THIS WITH TOKEN"}
    with open("secrets.json", "w") as outfile:
        json.dump(secretsDict, outfile)
    print("Add your token to secrets.json")
    exit()

logging.basicConfig()
bot = commands.Bot(command_prefix=prefsDict["commandPrefix"], description="A Discord bot made in Python using discord.py")

#List of cogs to be loaded
cogsList = {
    "basic",
    "color",
    "admin",
    "search"
    }

cogsStatus = {}

@bot.event
async def on_ready():
    print("--------------------")
    print(bot.user.name + " has started!")
    print("--------------------")

    #Set the bots playing message to show use of the prefix
    await bot.change_presence(game=discord.Game(name="{}help".format(prefsDict["commandPrefix"])))

    #Try to load the cogs and note if they are successfully loaded or not
    for cog in cogsList:
        try:
            bot.load_extension("cogs." + cog)
            cogsStatus[cog] = "Online"
        except Exception as e:
            cogsStatus[cog] = "*Offline*"

@bot.event
async def on_member_join(member):
    print(member.name + " joined")
    #Add any new bots invited to the server to the designated bot role
    if(member.bot == True):
        try:
            role = discord.utils.get(member.server.roles, name="Skynet")
            await bot.add_roles(member, role)
        except discord.Forbidden:
            print("I don't have permissions to add roles")

@bot.event
async def on_member_remove(member):
    print(member.name + " left")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command(hidden=True)
async def status():
    """Check status of cogs"""
    s=""
    for cog in cogsStatus:
        s += cog + ": " + cogsStatus[cog] + "\n"
    await bot.say(s)

@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def load(cog):
    """Load an cog"""
    try:
        bot.load_extension("cogs." + cog)
        cogsStatus[cog] = "Online"
        await bot.say(cog + " loaded :thumbsup:")
    except (AttributeError, ImportError) as e:
        await bot.say(str(e))

@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def unload(cog):
    """Unload an cog"""
    try:
        bot.unload_extension("cogs." + cog)
        cogsStatus[cog] = "*Offline*"
        await bot.say(cog + " unloaded :thumbsdown:")
    except (AttributeError, ImportError) as e:
        await bot.say(str(e))

@bot.event
async def on_command_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await bot.send_message(ctx.message.channel, content="This command is on cooldown. Try again in {0:.2f}s.".format(error.retry_after))

bot.run(secretsDict["token"])
