import logging

import discord
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class pokemon(commands.Cog):
    """Commands for Poke API"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemon(self, ctx, text: str):
        """Search for a Pokemon by name or id"""
        req = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(text))
        data = req.json()
        req = requests.get(data["species"]["url"])
        species_data = req.json()

        name = data["name"].capitalize()
        pokemon_id = data["id"]
        thumbnail = data["sprites"]["front_default"]

        for temp in species_data["flavor_text_entries"]:
            if temp["language"]["name"] == "en":
                flavor_text = temp["flavor_text"]
                break

        embedMessage = discord.Embed(title=flavor_text, colour=0x87CEEB)
        embedMessage.set_author(name="{}\t\t#{}".format(name, pokemon_id))
        embedMessage.set_thumbnail(url=thumbnail)

        for stat in data["stats"]:
            embedMessage.add_field(
                name=stat["stat"]["name"], value=stat["base_stat"], inline=True
            )

        embedMessage.set_footer(text="All data from https://pokeapi.co/")

        await ctx.send(embed=embedMessage)


def setup(bot):
    bot.add_cog(pokemon(bot))
