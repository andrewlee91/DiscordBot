import discord
from discord.ext import commands
import json
import urllib
import aiohttp
import os

class admin:
    """Admin only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    async def setprefix(self, ctx):
        """Set prefix for commands"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.say("You must specify a prefix")
        elif len(t[1]) > 2:
            await self.bot.say("You can only have 2 characters maximum set as a prefix")
        else:
            try:
                #Set the new prefix with the bot then save to to prefs.json
                self.bot.command_prefix = t[1]
                prefsDict = json.load(open("prefs.json"))
                prefsDict["commandPrefix"] = t[1]
                with open("prefs.json", "w") as fp:
                    json.dump(prefsDict, fp, indent=4)
                await self.bot.say("Prefix was set as {}".format(prefsDict["commandPrefix"]))
            except Exception as ex:
                await self.bot.say(str(ex))

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    async def setname(self, ctx):
        """Set the bots nickname"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.change_nickname(ctx.message.server.me, None)
            await self.bot.say("Name set to default")
        else:
            name = t[1]
            await self.bot.change_nickname(ctx.message.server.me, name)
            await self.bot.say("Name set to {}".format(t[1]))

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    async def setgame(self, ctx):
        """Set the bots playing status message"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.change_nickname(ctx.message.server.me, None)
            await self.bot.say("Name set to default")
        else:
            game = t[1]
            await self.bot.change_presence(game=discord.Game(name=game))
            await self.bot.say("Game set to {}".format(str(game)))

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    async def setavatar(self, ctx):
        """Set the bots avatar"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.say("Name set to default")
        else:
            link = t[1]
            async with aiohttp.get(link) as img:
                with open("avatar.png", "wb") as f:
                    f.write(await img.read())
            with open("avatar.png", "rb") as f:
                await self.bot.edit_profile(avatar=f.read())
            os.remove("avatar.png")
            await self.bot.say("New avatar set!")

def setup(bot):
    bot.add_cog(admin(bot))
