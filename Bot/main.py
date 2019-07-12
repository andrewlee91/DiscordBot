import configparser
import logging
import os
from datetime import datetime

import discord
from discord.ext import commands

bot_directory = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config_path = "{}/config.ini".format(bot_directory)

logging.basicConfig(
    filename="{}/error.log".format(bot_directory),
    filemode="a",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def Load_Config():
    if os.path.isfile(config_path):
        config.read(config_path)
    else:
        config["DEFAULT"] = {
            "prefix": "f!",
            "isblacklistenabled": True,
            "islogenabled": True,
        }

        with open(config_path, "w") as config_file:
            config.write(config_file)


def Log_Message(message):
    date = datetime.now().strftime("%d-%b-%y")
    time = datetime.now().strftime("%H:%M:%S")
    log_directory = "{}/logs/{}.txt".format(bot_directory, date)
    with open(log_directory, "a") as log_file:
        log_file.write(
            "{time} - {author} (id: {author_id}) - {message}\n".format(
                time=time,
                author=message.author,
                author_id=message.author.id,
                message=message.content,
            )
        )


def Is_Word_In_Blacklist(message):
    with open("{}/blacklist.txt".format(bot_directory)) as blacklist:
        for word in blacklist:
            if message.content.lower().find(word):
                return True
        return False


Load_Config()
bot = commands.Bot(command_prefix=config["DEFAULT"]["prefix"], help_command=None)


@bot.event
async def on_ready():
    # Check if logs directory exists; if it doesn't then create it
    if not os.path.isdir("{}/logs".format(bot_directory)):
        os.makedirs("{}/logs".format(bot_directory))

    # Get the list of cogs available and check if unwanted files are still lingering
    cogsList = os.listdir("{}/cogs".format(bot_directory))
    if "utils" in cogsList:
        cogsList.remove("utils")

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
        activity=discord.Game(name="{}help".format(config["DEFAULT"]["prefix"]))
    )

    # Log this just for reference
    logging.error(
        "{} has started using version {}".format(bot.user.name, discord.__version__)
    )


@bot.event
async def on_message(message):
    config.read(config_path)
    is_blacklist_enabled = config.getboolean("DEFAULT", "isblacklistenabled")
    is_log_enabled = config.getboolean("DEFAULT", "islogenabled")

    is_message_blacklisted = False

    # Log before we check for blacklist so we catch anyone being bad 🙂
    if is_log_enabled:
        Log_Message(message)

    # Removed blacklist code because it was deleting every message

    if not is_message_blacklisted and not message.author.bot:
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
async def on_command_error(ctx, error):
    """Command errors"""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "This command is on cooldown. Try again in {0:.2f}s.".format(
                error.retry_after
            )
        )
    else:
        logging.error(error)


bot.run(os.environ["DISCORD_TOKEN"])
