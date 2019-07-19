import logging
import random

import discord
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class pokemon(commands.Cog):
    """Commands for Poke API"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def pokemon(self, ctx):
        """Search for a Pokemon by name or id"""
        if ctx.invoked_subcommand is None:
            # For some reason I couldn't get subcommands to work when I passed an extra argument like I normally do
            # so I'm just extracting it from the message context instead even if it looks ugly
            text = ctx.message.content.split()[1]

            req = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(text))
            data = req.json()
            req = requests.get(data["species"]["url"])
            species_data = req.json()

            name = data["name"].capitalize()
            pokemon_id = data["id"]
            rand = random.randint(0, 450)
            if rand == 450:
                thumbnail = data["sprites"]["front_shiny"]
            else:
                thumbnail = data["sprites"]["front_default"]

            for temp in species_data["flavor_text_entries"]:
                if temp["language"]["name"] == "en":
                    flavor_text = temp["flavor_text"]
                    break

            temp = []
            for t in data["types"]:
                temp.append(t["type"]["name"].capitalize())
            pokemon_type = ", ".join(temp)

            hp = data["stats"][5]["base_stat"]
            attack = data["stats"][4]["base_stat"]
            special_attack = data["stats"][2]["base_stat"]
            defence = data["stats"][3]["base_stat"]
            special_defence = data["stats"][1]["base_stat"]
            speed = data["stats"][0]["base_stat"]

            temp = []
            for t in data["abilities"]:
                temp.append(t["ability"]["name"].capitalize())
            abilities = ", ".join(temp)

            embedMessage = discord.Embed(title=flavor_text, colour=0x87CEEB)
            embedMessage.set_author(name="#{} - {}".format(pokemon_id, name))
            embedMessage.set_thumbnail(url=thumbnail)

            embedMessage.add_field(name="Type", value=pokemon_type, inline=False)
            embedMessage.add_field(name="HP", value=hp, inline=True)
            embedMessage.add_field(name="Attack", value=attack, inline=True)
            embedMessage.add_field(
                name="Special Attack", value=special_attack, inline=True
            )
            embedMessage.add_field(name="Defence", value=defence, inline=True)
            embedMessage.add_field(
                name="Special Defence", value=special_defence, inline=True
            )
            embedMessage.add_field(name="Speed", value=speed, inline=True)
            embedMessage.add_field(name="Abilities", value=abilities, inline=False)

            embedMessage.set_footer(text="All data from https://pokeapi.co/")

            await ctx.send(embed=embedMessage)

    @pokemon.command()
    async def type(self, ctx, text: str):
        """Search for a Pokemon type"""
        req = requests.get("https://pokeapi.co/api/v2/type/{}".format(text))
        data = req.json()

        damage_type = data["move_damage_class"]["name"].capitalize()

        temp = []
        for t in data["damage_relations"]["double_damage_from"]:
            temp.append(t["name"].capitalize())
        double_damage_from = ", ".join(temp)

        temp = []
        for t in data["damage_relations"]["double_damage_to"]:
            temp.append(t["name"].capitalize())
        double_damage_to = ", ".join(temp)

        temp = []
        for t in data["damage_relations"]["half_damage_from"]:
            temp.append(t["name"].capitalize())
        half_damage_from = ", ".join(temp)

        temp = []
        for t in data["damage_relations"]["half_damage_to"]:
            temp.append(t["name"].capitalize())
        half_damage_to = ", ".join(temp)

        if data["damage_relations"]["no_damage_from"]:
            temp = []
            for t in data["damage_relations"]["no_damage_from"]:
                temp.append(t["name"].capitalize())
            no_damage_from = ", ".join(temp)
        else:
            no_damage_from = "None"

        if data["damage_relations"]["no_damage_to"]:
            temp = []
            for t in data["damage_relations"]["no_damage_to"]:
                temp.append(t["name"].capitalize())
            no_damage_to = ", ".join(temp)
        else:
            no_damage_to = "None"

        embedMessage = discord.Embed(
            title="Attack type: {}".format(damage_type), colour=0x87CEEB
        )
        embedMessage.set_author(name=text.capitalize())

        embedMessage.add_field(
            name="Double Damage To", value=double_damage_to, inline=True
        )
        embedMessage.add_field(
            name="Double Damage From", value=double_damage_from, inline=True
        )
        embedMessage.add_field(name="Half Damage To", value=half_damage_to, inline=True)
        embedMessage.add_field(
            name="Half Damage From", value=half_damage_from, inline=True
        )
        embedMessage.add_field(name="No Damage To", value=no_damage_to, inline=True)
        embedMessage.add_field(name="No Damage From", value=no_damage_from, inline=True)

        embedMessage.set_footer(text="All data from https://pokeapi.co/")

        await ctx.send(embed=embedMessage)

    @pokemon.command()
    async def ability(self, ctx, text: str):
        """Search for a Pokemon ability"""
        req = requests.get("https://pokeapi.co/api/v2/ability/{}".format(text.lower()))
        data = req.json()

        name = data["name"].capitalize()
        description = data["effect_entries"][0]["effect"]

        embedMessage = discord.Embed(title=description, colour=0x87CEEB)
        embedMessage.set_author(name=name)

        embedMessage.set_footer(text="All data from https://pokeapi.co/")

        await ctx.send(embed=embedMessage)


def setup(bot):
    bot.add_cog(pokemon(bot))
