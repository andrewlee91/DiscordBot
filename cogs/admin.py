import discord
from discord.ext import commands
import json
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
        else:
            name = t[1]
            await self.bot.change_nickname(ctx.message.server.me, name)

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    async def setgame(self, ctx):
        """Set the bots playing status message"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.change_presence(game=discord.Game(name=None))
        else:
            await self.bot.change_presence(game=discord.Game(name=t[1]))

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin")
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def setavatar(self, ctx):
        """Set the bots avatar"""
        t = ctx.message.content.split(" ", 1)
        if len(t) == 1:
            await self.bot.say("Please use a valid image link! It must be .jpg or .png")
        else:
            try:
                link = t[1]
                async with aiohttp.get(link) as img:
                    with open("avatar.png", "wb") as f:
                        f.write(await img.read())
                with open("avatar.png", "rb") as f:
                    await self.bot.edit_profile(avatar=f.read())
                os.remove("avatar.png")
                await self.bot.say("New avatar set!")
            except Exception as e:
                await self.bot.say(str(e))

def setup(bot):
    bot.add_cog(admin(bot))
    