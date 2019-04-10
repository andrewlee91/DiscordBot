import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class help(commands.Cog):
    """Cog for the help command"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        """Help command"""
        if ctx.invoked_subcommand is None:
            embedMessage = discord.Embed(
                title="To view the commands in each group type {}help <group>".format(
                    self.bot.command_prefix
                ),
                colour=0x87CEEB,
            )
            embedMessage.set_author(
                name="{}'s commands!".format(self.bot.user.name),
                icon_url=self.bot.user.avatar_url,
            )

            embedMessage.add_field(name="Basic", value="Basic commands", inline=True)
            embedMessage.add_field(
                name="Color", value="Set your own color", inline=True
            )
            embedMessage.add_field(
                name="Search", value="Search various websites", inline=True
            )
            embedMessage.add_field(
                name="RemindMe", value="Set your own reminders", inline=True
            )
            embedMessage.add_field(name="Admin", value="Admin only!", inline=True)
            embedMessage.add_field(
                name="Twitter", value="Twitter commands", inline=True
            )

            embedMessage.set_footer(text="https://github.com/andrewlee91/DiscordBot")

            await ctx.send(embed=embedMessage)

    @help.command()
    async def basic(self, ctx):
        """Basic subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="Basic commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(
            name="avatar", value="Post yours or mentioned users avatar", inline=False
        )
        embedMessage.add_field(
            name="choose",
            value="Choose between options (seperated by commas)",
            inline=False,
        )
        embedMessage.add_field(
            name="eightball", value="Ask the eightball a question", inline=False
        )
        embedMessage.add_field(name="flip", value="Flip a coin", inline=False)
        embedMessage.add_field(
            name="roll", value="Roll a dice (d4, d6, d8, d10, d12, d20)", inline=False
        )
        embedMessage.add_field(
            name="rps", value="Play Rock, Paper, Scissors", inline=False
        )
        embedMessage.add_field(
            name="say", value="Make the bot say something", inline=False
        )

        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)

    @help.command()
    async def color(self, ctx):
        """Color subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="Color commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(
            name="color",
            value="teal, dark_teal, green, dark_green, blue, dark_blue, purple, dark_purple, magenta, dark_magenta, gold, dark_gold, orange, dark_orange, red, dark_red",
            inline=False,
        )

        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)

    @help.command()
    async def admin(self, ctx):
        """Admin subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="Admin only commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(name="setprefix", value="2 characters max", inline=False)
        embedMessage.add_field(
            name="setname", value="Leave blank to reset to original name", inline=False
        )
        embedMessage.add_field(
            name="setavatar",
            value="Must be .jpg or .png url. 60 second cooldown",
            inline=False,
        )

        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)

    @help.command()
    async def search(self, ctx):
        """Search subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="Search commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(
            name="osu", value="Get your Osu! stats based on username", inline=False
        )
        embedMessage.add_field(
            name="taiko",
            value="Get your Osu!Taiko! stats based on username",
            inline=False,
        )
        embedMessage.add_field(
            name="ctb",
            value="Get your Osu!Catch the Beat! stats based on username",
            inline=False,
        )
        embedMessage.add_field(
            name="mania",
            value="Get your Osu!Mania! stats based on username",
            inline=False,
        )
        embedMessage.add_field(
            name="urban", value="Search Urban Dictionary", inline=False
        )
        embedMessage.add_field(
            name="anime", value="Search AniList for anime", inline=False
        )
        embedMessage.add_field(
            name="manga", value="Search AniList for manga", inline=False
        )
        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)

    @help.command()
    async def remindme(self, ctx):
        """RemindMe subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="RemindMe commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(
            name="remindme",
            value="{}remindme <length> <minute/hour/day/month> <text>".format(
                self.bot.command_prefix
            ),
            inline=False,
        )

        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)

    @help.command()
    async def twitter(self, ctx):
        """Twitter subcommand"""
        embedMessage = discord.Embed(
            title="All commands use the {} prefix".format(self.bot.command_prefix),
            colour=0x87CEEB,
        )
        embedMessage.set_author(
            name="Twitter commands!", icon_url=self.bot.user.avatar_url
        )

        embedMessage.add_field(
            name="follow", value="Get updated when someone tweets", inline=False
        )
        embedMessage.add_field(
            name="unfollow", value="Remove a user from the following list", inline=False
        )

        embedMessage.set_footer(
            text="{}help to see all command groups".format(self.bot.command_prefix)
        )

        await ctx.send(embed=embedMessage)


def setup(bot):
    bot.add_cog(help(bot))
