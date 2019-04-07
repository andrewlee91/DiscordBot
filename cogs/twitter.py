import asyncio
import json
import logging

import discord
from discord.ext import commands

from cogs.utils import twitterstreamer

logger = logging.getLogger(__name__)


class twitter:
    """Twitter"""

    def __init__(self, bot):
        self.bot = bot

        try:
            followingList = json.load(open("followinglist.json"))
        except:
            followingList = {}
            with open("followinglist.json", "w") as outfile:
                json.dump(followingList, outfile)

        try:
            tweets = json.load(open("tweets.json"))
        except:
            tweets = {}
            with open("tweets.json", "w") as outfile:
                json.dump(tweets, outfile)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def follow(self, ctx, username: str):
        """Follow a user"""
        status = twitterstreamer.FollowUser(username, ctx.message.channel.id)
        await self.bot.say(status)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def unfollow(self, username: str):
        """Unfollow a user"""
        status = twitterstreamer.UnfollowUser(username)
        await self.bot.say(status)

    async def check_tweets(self):
        """Check Tweets"""
        while not self.bot.is_closed:
            tweets = json.load(open("tweets.json"))
            if len(tweets) > 0:
                followingList = json.load(open("followinglist.json"))
                for t in tweets:
                    channelID = followingList[tweets[t][0]][1]
                    await self.bot.send_message(
                        self.bot.get_channel(channelID), tweets[t][1]
                    )

            # Clear tweets because we've already posted them all
            tweets = {}
            with open("tweets.json", "w") as outfile:
                json.dump(tweets, outfile)

            await asyncio.sleep(5)


def setup(bot):
    loop = asyncio.get_event_loop()
    loop.create_task(twitter(bot).check_tweets())
    bot.add_cog(twitter(bot))
