import logging
import random

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class basic:
    """Basic commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, *, text: str):
        """Make the bot say something"""
        await self.bot.say(text)

    @commands.command(pass_context=True)
    async def avatar(self, ctx):
        """Post yours or mentioned users avatar"""
        if len(ctx.message.mentions) > 0:
            await self.bot.say(str(ctx.message.mentions[0].avatar_url))
        else:
            await self.bot.say(str(ctx.message.author.avatar_url))

    @commands.command(pass_context=True)
    async def choose(self, ctx):
        """Choose between options (seperated by commas)"""
        t = str(ctx.message.content).split(" ", 1)[1]
        temp = t.split(",")
        r = random.randint(0, len(temp) - 1)
        await self.bot.say("I choose... **{}** :thinking:".format(temp[r]))

    @commands.group(pass_context=True)
    async def roll(self, ctx):
        """Roll the dice (d6 default)"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 6))))

    @roll.command(pass_context=True)
    async def d4(self):
        """Roll a D4 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 4))))

    @roll.command(pass_context=True)
    async def d6(self):
        """Roll a D6 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 6))))

    @roll.command(pass_context=True)
    async def d8(self):
        """Roll a D8 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 8))))

    @roll.command(pass_context=True)
    async def d10(self):
        """Roll a D10 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 10))))

    @roll.command(pass_context=True)
    async def d12(self):
        """Roll a D12 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 12))))

    @roll.command(pass_context=True)
    async def d20(self):
        """Roll a D20 dice"""
        await self.bot.say("You rolled... **{}** :game_die:".format(str(random.randint(1, 20))))

    @commands.command()
    async def flip(self):
        """Flip a coin"""
        r = random.randint(1, 2)
        if r == 1:
            await self.bot.say("It landed on... **Heads**")
        elif r == 2:
            await self.bot.say("It landed on... **Tails**")

    @commands.command(pass_context=True)
    async def rps(self, ctx):
        """Play rock-paper-scissors"""
        userChoice = ctx.message.content.split(" ", 1)
        userChoice = userChoice[1].lower()

        if userChoice != "rock" and userChoice != "paper" and userChoice != "scissors":
            await self.bot.say("You can only choose from rock, paper or scissors")
        else:
            temp = random.randint(1, 3)
            if temp == 1:
                botChoice = "rock"
            elif temp == 2:
                botChoice = "paper"
            elif temp == 3:
                botChoice = "scissors"

           #This is kind of ugly but it works
            if userChoice == botChoice:
                await self.bot.say("I choose **{}**. The game was a tie!".format(botChoice))
            elif userChoice == "rock":
                if botChoice == "paper":
                    await self.bot.say("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "scissors":
                    await self.bot.say("I choose **{}**. You win!".format(botChoice))
            elif userChoice == "paper":
                if botChoice == "scissors":
                    await self.bot.say("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "rock":
                    await self.bot.say("I choose **{}**. You win!".format(botChoice))
            elif userChoice == "scissors":
                if botChoice == "rock":
                    await self.bot.say("I choose **{}**. I win!".format(botChoice))
                elif botChoice == "paper":
                    await self.bot.say("I choose **{}**. You win!".format(botChoice))

    @commands.command(pass_context=True)
    async def eightball(self, ctx):
        """Ask the eightball a question"""
        t = str(ctx.message.content).split(" ", 1)
        if len(t) == 1:
            await self.bot.say("You must ask a question!")
        else:
            r = random.randint(1, 20)
            await self.bot.say("**{}** :8ball:".format(eightballDict(r)))

def eightballDict(x):
    return {
        1:"It is certain",
        2:"It is decidedly so",
        3:"Without a doubt",
        4:"Yes, definitely",
        5:"You may rely on it",
        6:"As I see it, yes",
        7:"Most likely",
        8:"Outlook good",
        9:"Yes",
        10:"Signs point to yes",
        11:"Reply hazy try again",
        12:"Ask again later",
        13:"Better not tell you now",
        14:"Cannot predict now",
        15:"Concentrate and ask again",
        16:"Don't count on it",
        17:"My reply is no",
        18:"My sources say no",
        19:"Outlook not so good",
        20:"Very doubtful"
    }[x]

def setup(bot):
    bot.add_cog(basic(bot))
