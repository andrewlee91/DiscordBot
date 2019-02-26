import discord
from discord.ext import commands
import aiohttp
import os


class search:
    """Search commands for various websites and games"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def osu(self, ctx):
        """Get your Osu!standard stats"""
        t = ctx.message.content.split(" ", 1)
        if len(t) > 1:
            link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&countryrank".format(t[1])
            async with aiohttp.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
            channel = ctx.message.channel
            await self.bot.send_file(channel, "osu.png",filename="osu.png",content="")
            os.remove("osu.png")

    @commands.command(pass_context=True)
    async def taiko(self, ctx):
        """Get your Osu!taiko! stats"""
        t = ctx.message.content.split(" ", 1)
        if len(t) > 1:
            link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=1&countryrank".format(t[1])
            async with aiohttp.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
            channel = ctx.message.channel
            await self.bot.send_file(channel, "osu.png",filename="osu.png",content="")
            os.remove("osu.png")

    @commands.command(pass_context=True)
    async def ctb(self, ctx):
        """Get your Osu!Catch the Beat! stats"""
        t = ctx.message.content.split(" ", 1)
        if len(t) > 1:
            link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=2&countryrank".format(t[1])
            async with aiohttp.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
            channel = ctx.message.channel
            await self.bot.send_file(channel, "osu.png",filename="osu.png",content="")
            os.remove("osu.png")

    @commands.command(pass_context=True)
    async def mania(self, ctx):
        """Get your Osu!Mania! stats"""
        t = ctx.message.content.split(" ", 1)
        if len(t) > 1:
            link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=3&countryrank".format(t[1])
            async with aiohttp.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
            channel = ctx.message.channel
            await self.bot.send_file(channel, "osu.png",filename="osu.png",content="")
            os.remove("osu.png")

def setup(bot):
    bot.add_cog(search(bot))
