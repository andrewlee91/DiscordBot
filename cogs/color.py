import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

colorList = {
    "teal"          : discord.Color.teal(),
    "dark_teal"     : discord.Colour.dark_teal(),
    "green"         : discord.Colour.green(),
    "dark_green"    : discord.Colour.dark_green(),
    "blue"          : discord.Colour.blue(),
    "dark_blue"     : discord.Colour.dark_blue(),
    "purple"        : discord.Colour.purple(),
    "dark_purple"   : discord.Colour.dark_purple(),
    "magenta"       : discord.Colour.magenta(),
    "dark_magenta"  : discord.Colour.dark_magenta(),
    "gold"          : discord.Colour.gold(),
    "dark_gold"     : discord.Colour.dark_gold(),
    "orange"        : discord.Colour.orange(),
    "dark_orange"   : discord.Colour.dark_orange(),
    "red"           : discord.Colour.red(),
    "dark_red"      : discord.Colour.dark_red()
}

class color:
    """Commands for setting your own color"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def color(self, ctx):
        """Change your color"""
        colorSelection = ctx.message.content.split(" ", 1)
        if len(colorSelection) == 1:
            #Change color to the default grey
            for role in ctx.message.author.roles:
                if(str(role) in colorList):
                    await self.bot.remove_roles(ctx.message.author, role)
        elif colorSelection[1].lower() in colorList:
            colorSelection = colorSelection[1].lower()
            #Remove all previous color roles from the user
            for role in ctx.message.author.roles:
                if(str(role) in colorList):
                    await self.bot.remove_roles(ctx.message.author, role)
            #Determine if the color role already exists, if not then create it
            role = discord.utils.get(ctx.message.author.server.roles, name=colorSelection)
            if role is None:
                color = await self.bot.create_role(ctx.message.server)
                await self.bot.edit_role(ctx.message.server, color, name=colorSelection, colour=colorList[colorSelection])
            #Give the author the color role
            role = discord.utils.get(ctx.message.author.server.roles, name=colorSelection)
            await self.bot.add_roles(ctx.message.author, role)
            await self.bot.say("Lookin' good :sunglasses:")

def setup(bot):
    bot.add_cog(color(bot))
