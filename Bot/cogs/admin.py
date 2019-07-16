import configparser
import logging
import os

import aiohttp
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

bot_directory = "{}/Bot".format(os.getcwd())

config = configparser.ConfigParser()


class admin(commands.Cog):
    """Admin only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Admin")
    async def setprefix(self, ctx, prefix: str):
        """Set prefix for commands"""
        if len(prefix) > 2:
            await ctx.send("You can only have 2 characters maximum set as a prefix")
            return

        # Set the new prefix with the bot then save to to prefs.json
        self.bot.command_prefix = prefix
        config.read("{}/config.ini".format(bot_directory))
        config["DEFAULT"]["prefix"] = prefix
        with open("{}/config.ini".format(bot_directory), "w") as config_file:
            config.write(config_file)
        await ctx.send("Prefix was set as {}".format(config["DEFAULT"]["prefix"]))

        # Set the playing message to use the new prefix
        await self.bot.change_presence(
            activity=discord.Game(name="{}help".format(config["DEFAULT"]["prefix"]))
        )

    @commands.command()
    @commands.has_any_role("Admin")
    @commands.cooldown(1, 30, commands.BucketType.default)
    async def setname(self, ctx, *, name: str = None):
        """Set the bots nickname"""
        await ctx.guild.me.edit(nick=name)

    @commands.command()
    @commands.has_any_role("Admin")
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def setavatar(self, ctx, link: str):
        """Set the bots avatar"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as img:
                    with open("avatar.png", "wb") as f:
                        f.write(await img.read())
            with open("avatar.png", "rb") as f:
                await self.bot.user.edit(avatar=f.read())
            os.remove("avatar.png")
            await ctx.send("New avatar set!")
        except Exception as e:
            await ctx.send(str(e))

    @commands.command()
    @commands.has_any_role("Admin")
    async def toggleblacklist(self, ctx):
        """Toggle the blacklist on and off"""
        config.read("{}/config.ini".format(bot_directory))
        blacklist_enabled = config.getboolean("MODERATION", "blacklistenabled")
        if blacklist_enabled:
            config["MODERATION"]["blacklistenabled"] = "False"
            await ctx.send("Blacklist is now disabled")
        else:
            config["MODERATION"]["blacklistenabled"] = "True"
            await ctx.send("Blacklist is now enabled")

        with open("{}/config.ini".format(bot_directory), "w") as config_file:
            config.write(config_file)

    @commands.command()
    @commands.has_any_role("Admin")
    async def togglelog(self, ctx):
        """Toggle the chat logs on and off"""
        config.read("{}/config.ini".format(bot_directory))
        log_enabled = config.getboolean("MODERATION", "logenabled")
        if log_enabled:
            config["MODERATION"]["logenabled"] = "False"
            await ctx.send("Chat logs are now disabled")
        else:
            config["MODERATION"]["logenabled"] = "True"
            await ctx.send("Chat logs now enabled")

        with open("{}/config.ini".format(bot_directory), "w") as config_file:
            config.write(config_file)


def setup(bot):
    bot.add_cog(admin(bot))
