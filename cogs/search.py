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

    @commands.command()
    async def anime(self, *, text: str):
        """Search AniList for anime"""
        query = """
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                episodes
                duration
                status
                genres
                averageScore
                coverImage {
                    large
                }
            }
        }
        """

        variables = {"search": text}

        response = requests.post(
            "https://graphql.anilist.co", json={"query": query, "variables": variables}
        )

        rateLimitRemaining = int(response.headers["X-RateLimit-Remaining"])

        # Rate limiting is currently set to 90 requests per minute
        # If you go over the rate limit you'll receive a 1-minute timeout
        # https://anilist.gitbook.io/anilist-apiv2-docs/overview/rate-limiting
        if rateLimitRemaining > 0:
            animeJSON = response.json()["data"]["Media"]

            description = animeJSON["description"]
            description = description.replace("<br>", "")
            genres = ""
            for g in animeJSON["genres"]:
                genres += "{}, ".format(g)

            embed = discord.Embed(
                title="{} / {}".format(
                    animeJSON["title"]["romaji"], animeJSON["title"]["native"]
                ),
                url="https://anilist.co/anime/{}".format(animeJSON["id"]),
                description=description,
            )
            embed.set_thumbnail(url=animeJSON["coverImage"]["large"])
            embed.add_field(
                name="Episode Count", value=animeJSON["episodes"], inline=True
            )
            embed.add_field(
                name="Duration",
                value="{} minutes per episode".format(animeJSON["duration"]),
                inline=True,
            )
            embed.add_field(name="Status", value=animeJSON["status"], inline=True)
            embed.add_field(name="Genres", value=genres[:-2], inline=True)
            embed.add_field(
                name="Average Score", value=animeJSON["averageScore"], inline=True
            )
            embed.set_footer(text="Powered by anilist.co")
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(
                "The bot is currently being rate limited :( Try again in {} seconds".format(
                    response.headers["Retry-After"]
                )
            )

    @commands.command()
    async def manga(self, *, text: str):
        """Search AniList for manga"""
        query = """
        query ($search: String) {
            Media (search: $search, type: MANGA) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                chapters
                volumes
                status
                genres
                averageScore
                coverImage {
                    large
                }
            }
        }
        """

        variables = {"search": text}

        response = requests.post(
            "https://graphql.anilist.co", json={"query": query, "variables": variables}
        )

        rateLimitRemaining = int(response.headers["X-RateLimit-Remaining"])

        # Rate limiting is currently set to 90 requests per minute
        # If you go over the rate limit you'll receive a 1-minute timeout
        # https://anilist.gitbook.io/anilist-apiv2-docs/overview/rate-limiting
        if rateLimitRemaining > 0:
            mangaJSON = response.json()["data"]["Media"]

            description = mangaJSON["description"]
            description = description.replace("<br>", "")
            genres = ""
            for g in mangaJSON["genres"]:
                genres += "{}, ".format(g)

            embed = discord.Embed(
                title="{} / {}".format(
                    mangaJSON["title"]["romaji"], mangaJSON["title"]["native"]
                ),
                url="https://anilist.co/manga/{}".format(mangaJSON["id"]),
                description=description,
            )
            embed.set_thumbnail(url=mangaJSON["coverImage"]["large"])
            embed.add_field(name="Chapters", value=mangaJSON["chapters"], inline=True)
            embed.add_field(name="Volumes", value=mangaJSON["volumes"], inline=True)
            embed.add_field(name="Status", value=mangaJSON["status"], inline=True)
            embed.add_field(name="Genres", value=genres[:-2], inline=True)
            embed.add_field(
                name="Average Score", value=mangaJSON["averageScore"], inline=True
            )
            embed.set_footer(text="Powered by anilist.co")
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(
                "The bot is currently being rate limited :( Try again in {} seconds".format(
                    response.headers["Retry-After"]
                )
            )


def setup(bot):
    bot.add_cog(search(bot))
