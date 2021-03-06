import logging
import os

import aiohttp
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class games(commands.Cog):
    """Commands to look up stats in various games"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def osu(self, ctx, username: str):
        """Get your Osu!standard stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&countryrank".format(
            username
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
        await ctx.send(file=discord.File("osu.png"))
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def taiko(self, ctx, username: str):
        """Get your Osu!taiko! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=1&countryrank".format(
            username
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
        await ctx.send(file=discord.File("osu.png"))
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def ctb(self, ctx, username: str):
        """Get your Osu!Catch the Beat! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=2&countryrank".format(
            username
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
        await ctx.send(file=discord.File("osu.png"))
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def mania(self, ctx, username: str):
        """Get your Osu!Mania! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=3&countryrank".format(
            username
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as img:
                with open("osu.png", "wb") as f:
                    f.write(await img.read())
        await ctx.send(file=discord.File("osu.png"))
        os.remove("osu.png")


def setup(bot):
    bot.add_cog(games(bot))
