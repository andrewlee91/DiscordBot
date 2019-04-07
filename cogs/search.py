import logging
import os
import aiohttp
import json
import requests

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class search:
    """Search commands for various websites and games"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def osu(self, ctx, username: str):
        """Get your Osu!standard stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&countryrank".format(
            username
        )
        async with aiohttp.get(link) as img:
            with open("osu.png", "wb") as f:
                f.write(await img.read())
        channel = ctx.message.channel
        await self.bot.send_file(channel, "osu.png", filename="osu.png", content="")
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def taiko(self, ctx, username: str):
        """Get your Osu!taiko! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=1&countryrank".format(
            username
        )
        async with aiohttp.get(link) as img:
            with open("osu.png", "wb") as f:
                f.write(await img.read())
        channel = ctx.message.channel
        await self.bot.send_file(channel, "osu.png", filename="osu.png", content="")
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def ctb(self, ctx, username: str):
        """Get your Osu!Catch the Beat! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=2&countryrank".format(
            username
        )
        async with aiohttp.get(link) as img:
            with open("osu.png", "wb") as f:
                f.write(await img.read())
        channel = ctx.message.channel
        await self.bot.send_file(channel, "osu.png", filename="osu.png", content="")
        os.remove("osu.png")

    @commands.command(pass_context=True)
    async def mania(self, ctx, username: str):
        """Get your Osu!Mania! stats"""
        link = "http://lemmmy.pw/osusig/sig.php?colour=blue&uname={}&mode=3&countryrank".format(
            username
        )
        async with aiohttp.get(link) as img:
            with open("osu.png", "wb") as f:
                f.write(await img.read())
        channel = ctx.message.channel
        await self.bot.send_file(channel, "osu.png", filename="osu.png", content="")
        os.remove("osu.png")

    @commands.command()
    async def urban(self, *, term: str):
        """Search Urban Dictionary"""
        req = requests.get(
            "http://api.urbandictionary.com/v0/define?term={}".format(term)
        )
        # Get JSON data for the first result
        dictTerm = req.json()
        dictTerm = dictTerm["list"][0]

        word = dictTerm["word"]
        definition = dictTerm["definition"]
        example = dictTerm["example"]
        message = "{} \n\n *{}*".format(definition, example)

        # Get rid of any square brackets
        message = message.replace("[", "")
        message = message.replace("]", "")

        embed = discord.Embed()
        embed.add_field(name=word, value=message, inline=False)

        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(search(bot))
