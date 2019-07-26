import asyncio
import json
import logging
import os
import time

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

data_directory = "{}/Bot/data".format(os.getcwd())
reminders_path = "{}/reminders.json".format(data_directory)

# Time conversions to seconds, includes variations for plurals
timeConversions = {
    "minute": 60,
    "minutes": 60,
    "hour": 3600,
    "hours": 3600,
    "day": 86400,
    "days": 86400,
    "month": 2592000,
    "months": 2592000,
}


class remindme(commands.Cog):
    """Remind me of stuff"""

    def __init__(self, bot):
        self.bot = bot

        # Check files
        if not os.path.isdir(data_directory):
            os.makedirs(data_directory)

        if os.path.isfile(reminders_path):
            remindersList = json.load(open(reminders_path))
        else:
            remindersList = {}
            with open(reminders_path, "w") as outfile:
                json.dump(remindersList, outfile)

        self.reminders_check = bot.loop.create_task(self.check_reminders())

    @commands.command()
    async def remindme(self, ctx, length: int, unit: str, *, text: str):
        """Sends you a reminder. Cannot be shorter than 1 minute"""
        # Check input
        if length < 1:
            await ctx.send("You must specify a time greater than 0.")
            return
        if unit.lower() not in timeConversions:
            await ctx.send("You must specify minute(s)/hour(s)/day(s)/month(s).")
            return
        if len(text) > 1000:
            await ctx.send("Reminder text is too long.")
            return

        # Calculate the time at which the bot should remind the user
        seconds = length * timeConversions[unit]
        currentTime = time.time()
        remindTime = currentTime + seconds

        # Get the user and channel ID
        userID = ctx.message.author.id
        channelID = ctx.message.channel.id

        # Save the reminder
        remindersList = json.load(open(reminders_path))
        remindersList[remindTime] = [text, userID, channelID]

        with open(reminders_path, "w") as outfile:
            json.dump(remindersList, outfile)

        await ctx.send("I'll remind you '{}' in {} {}".format(text, length, unit))

    async def check_reminders(self):
        """Check Reminders"""
        while not self.bot.is_closed():
            remindersList = json.load(open(reminders_path))
            if len(remindersList) > 0:
                tempDictionary = dict(remindersList)
                for reminder in remindersList:
                    temp = float(reminder)
                    if temp < time.time():
                        reminderText = remindersList[reminder][0]
                        userID = remindersList[reminder][1]
                        channelID = remindersList[reminder][2]
                        reminderMessage = "<@{}> {}".format(userID, reminderText)

                        channel = self.bot.get_channel(channelID)
                        await channel.send(reminderMessage)
                        del tempDictionary[reminder]
                with open(reminders_path, "w") as outfile:
                    json.dump(tempDictionary, outfile)
            await asyncio.sleep(5)


def setup(bot):
    bot.add_cog(remindme(bot))
