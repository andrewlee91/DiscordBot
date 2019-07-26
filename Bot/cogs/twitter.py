import asyncio
import json
import logging
import os

import discord
from discord.ext import commands
from utils import twitterstreamer

logger = logging.getLogger(__name__)

data_directory = "{}/Bot/data".format(os.getcwd())
tweets_path = "{}/tweets.json".format(data_directory)
followinglist_path = "{}/followinglist.json".format(data_directory)


class twitter(commands.Cog):
    """Twitter"""

    def __init__(self, bot):
        self.bot = bot

        twitterstreamer.Setup_Files()
        twitterstreamer.Start_Streamer()

        self.tweet_check = bot.loop.create_task(self.check_tweets())

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def follow(self, ctx, username: str):
        """Follow a user"""
        status = twitterstreamer.Follow_User(username, ctx.message.channel.id)
        await ctx.send(status)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.default)
    async def unfollow(self, ctx, username: str):
        """Unfollow a user"""
        status = twitterstreamer.Unfollow_User(username)
        await ctx.send(status)

    async def check_tweets(self):
        """Check Tweets"""
        while not self.bot.is_closed():
            tweets = json.load(open(tweets_path))
            if len(tweets) > 0:
                followingList = json.load(open(followinglist_path))
                for t in tweets:
                    channelID = followingList[tweets[t][0]][1]
                    channel = self.bot.get_channel(channelID)
                    await channel.send(tweets[t][1])

                # Clear tweets because we've already posted them all
                tweets = {}
                with open(tweets_path, "w") as outfile:
                    json.dump(tweets, outfile)

            await asyncio.sleep(5)


def setup(bot):
    bot.add_cog(twitter(bot))
