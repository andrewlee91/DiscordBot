import logging
import random
import requests

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class basic(commands.Cog):
    """Basic commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        """Get a joke from the joke api"""
        req = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = req.json()
        await ctx.send("{}\n\n{}".format(joke["setup"], joke["punchline"]))

    @commands.command()
    async def ron(self, ctx):
        """Get a Ron Swanson quote"""
        req = requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes")
        quote = req.json()
        await ctx.send(quote[0])

    @commands.command()
    async def say(self, ctx, *, text: str):
        """Make the bot say something"""
        await ctx.send(text)

    @commands.command()
    async def avatar(self, ctx):
        """Post yours or mentioned users avatar"""
        if len(ctx.message.mentions) > 0:
            await ctx.send(str(ctx.message.mentions[0].avatar_url))
        else:
            await ctx.send(str(ctx.message.author.avatar_url))

    @commands.command()
    async def choose(self, ctx, *, text: str):
        """Choose between options (seperated by commas)"""
        # Remove spaces and white space, split into a list and choose a random element
        text = text.strip()
        temp = text.split(",")
        await ctx.send(
            "I choose... **{}** :thinking:".format(
                temp[random.randint(0, len(temp) - 1)]
            )
        )

    @commands.group()
    async def roll(self, ctx, number: int = 6):
        """Roll the dice (d6 default)"""
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "You rolled... **{}** :game_die:".format(str(random.randint(1, number)))
            )

    @roll.command()
    async def d4(self, ctx):
        """Roll a D4 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 4)))
        )

    @roll.command()
    async def d6(self, ctx):
        """Roll a D6 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 6)))
        )

    @roll.command()
    async def d8(self, ctx):
        """Roll a D8 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 8)))
        )

    @roll.command()
    async def d10(self, ctx):
        """Roll a D10 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 10)))
        )

    @roll.command()
    async def d12(self, ctx):
        """Roll a D12 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 12)))
        )

    @roll.command()
    async def d20(self, ctx):
        """Roll a D20 dice"""
        await ctx.send(
            "You rolled... **{}** :game_die:".format(str(random.randint(1, 20)))
        )

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin"""
        rand = random.randint(1, 2)
        if rand == 1:
            await ctx.send("It landed on... **Heads**")
        elif rand == 2:
            await ctx.send("It landed on... **Tails**")

    @commands.command()
    async def rps(self, ctx, choice: str):
        """Play rock-paper-scissors"""
        userChoice = choice.lower()

        if userChoice != "rock" and userChoice != "paper" and userChoice != "scissors":
            await ctx.send("You can only choose from rock, paper or scissors")
        else:
            temp = random.randint(1, 3)
            if temp == 1:
                botChoice = "rock"
            elif temp == 2:
                botChoice = "paper"
            elif temp == 3:
                botChoice = "scissors"

            # This is kind of ugly but it works
            if userChoice == botChoice:
                await ctx.send("I choose **{}**. The game was a tie!".format(botChoice))
            elif userChoice == "rock":
                if botChoice == "paper":
                    await ctx.send("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "scissors":
                    await ctx.send("I choose **{}**. You win!".format(botChoice))
            elif userChoice == "paper":
                if botChoice == "scissors":
                    await ctx.send("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "rock":
                    await ctx.send("I choose **{}**. You win!".format(botChoice))
            elif userChoice == "scissors":
                if botChoice == "rock":
                    await ctx.send("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "paper":
                    await ctx.send("I choose **{}**. You win!".format(botChoice))

    @commands.command()
    async def eightball(self, ctx, *, text: str):
        """Ask the eightball a question"""
        await ctx.send("**{}** :8ball:".format(eightballDict(random.randint(1, 20))))


def eightballDict(x):
    return {
        1: "It is certain",
        2: "It is decidedly so",
        3: "Without a doubt",
        4: "Yes, definitely",
        5: "You may rely on it",
        6: "As I see it, yes",
        7: "Most likely",
        8: "Outlook good",
        9: "Yes",
        10: "Signs point to yes",
        11: "Reply hazy try again",
        12: "Ask again later",
        13: "Better not tell you now",
        14: "Cannot predict now",
        15: "Concentrate and ask again",
        16: "Don't count on it",
        17: "My reply is no",
        18: "My sources say no",
        19: "Outlook not so good",
        20: "Very doubtful",
    }[x]


def setup(bot):
    bot.add_cog(basic(bot))
