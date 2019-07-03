import json
import logging
import os

import discord
from discord.ext import commands

# prefs.json is used to store things like the command prefix and any channel ids
try:
    prefsDict = json.load(open("prefs.json"))
except Exception as e:
    prefsDict = {"commandPrefix": "f!"}
    with open("prefs.json", "w") as outfile:
        json.dump(prefsDict, outfile)

logging.basicConfig(
    filename="error.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

bot = commands.Bot(command_prefix=prefsDict["commandPrefix"], help_command=None)


@bot.event
async def on_ready():
    # Get the list of cogs available and check if unwanted files are still lingering
    bot_directory = os.path.dirname(os.path.realpath(__file__))
    cogsList = os.listdir("{}/cogs".format(bot_directory))
    if "utils" in cogsList:
        cogsList.remove("utils")
    if "__pycache__" in cogsList:
        cogsList.remove("__pycache__")
    # Try to load the cogs
    for cog in cogsList:
        # Trim .py from the end of the file names
        cog = cog[:-3]
        try:
            # cogs. is required to point to the correct directory
            bot.load_extension("cogs." + cog)
        except Exception as e:
            logging.error(str(e))
    # Set the bots playing message to show use of the prefix
    await bot.change_presence(
        activity=discord.Game(name="{}help".format(prefsDict["commandPrefix"]))
    )

    print("{} has started using version {}".format(bot.user.name, discord.__version__))


@bot.event
async def on_message(message):
    with open("blacklist.txt") as blacklist:
        if message.content in blacklist.read():
            author = message.author.id
            await message.channel.send("<@{}> that's a bad word".format(author))
            await message.delete()

    await bot.process_commands(message)


@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def load(ctx, cog: str):
    """Load an cog"""
    try:
        bot.load_extension("cogs." + cog)
        await ctx.send("{} loaded :thumbsup:".format(cog))
    except Exception as e:
        logging.error(str(e))
        await ctx.send(str(e))


@bot.command(hidden=True)
@commands.has_any_role("Admin")
async def unload(ctx, cog: str):
    """Unload an cog"""
    try:
        bot.unload_extension("cogs." + cog)
        await ctx.send("{} unloaded :thumbsdown:".format(cog))
    except Exception as e:
        logging.error(str(e))
        await ctx.send(str(e))


@bot.event
async def on_command_error(error, ctx):
    """Command errors"""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "This command is on cooldown. Try again in {0:.2f}s.".format(
                error.retry_after
            )
        )

    logging.error(error)


bot.run(os.environ["DISCORD_TOKEN"])
