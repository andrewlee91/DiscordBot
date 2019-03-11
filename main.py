import discord
from discord.ext import commands
import logging
import json
import os

#prefs.json is used to store things like the command prefix and any channel ids that need to be saved between sessions
try:
    prefsDict = json.load(open("prefs.json"))
except Exception as ex:
    prefsDict = { 
        "commandPrefix": "f!"
        }
    with open("prefs.json", "w") as outfile:
        json.dump(prefsDict, outfile)

logging.basicConfig()
bot = commands.Bot(command_prefix=prefsDict["commandPrefix"])
bot.remove_command("help")

@bot.event
async def on_ready():
    #Get the list of cogs available and check if pycache is still lingering
    cogsList = os.listdir("cogs")
    if "__pycache__" in cogsList:
        cogsList.remove("__pycache__")
    if "data" in cogsList:
        cogsList.remove("data")
    #Try to load the cogs
    for cog in cogsList:
        #Trim .py from the end of the file names
        cog = cog[:-3]
        try:
            #cogs. is required to point to the correct directory
            bot.load_extension("cogs." + cog)
        except Exception as e:
            print(str(e))
    #Set the bots playing message to show use of the prefix
    await bot.change_presence(game=discord.Game(name="{}help".format(prefsDict["commandPrefix"])))

    print("--------------------")
    print(bot.user.name + " has started!")
    print("--------------------")


@bot.event
async def on_member_join(member):
    #Add any new bots invited to the server to the designated bot role
    if member.bot == True:
        try:
            role = discord.utils.get(member.server.roles, name="Skynet")
            await bot.add_roles(member, role)
        except discord.Forbidden:
            print("I don't have permissions to add roles")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def load(cog):
    """Load an cog"""
    try:
        bot.load_extension("cogs." + cog)
        await bot.say(cog + " loaded :thumbsup:")
    except (AttributeError, ImportError) as e:
        await bot.say(str(e))

@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def unload(cog):
    """Unload an cog"""
    try:
        bot.unload_extension("cogs." + cog)
        await bot.say(cog + " unloaded :thumbsdown:")
    except (AttributeError, ImportError) as e:
        await bot.say(str(e))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content="This command is on cooldown. Try again in {0:.2f}s.".format(error.retry_after))

bot.run(os.environ["DISCORD_TOKEN"])
