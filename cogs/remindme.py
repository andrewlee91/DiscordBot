import asyncio
import json
import logging
import time

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

#Time conversions to seconds, includes variations for plurals
timeConversions = {
    "minute"    : 60,
    "minutes"   : 60,
    "hour"      : 3600,
    "hours"     : 3600,
    "day"       : 86400,
    "days"      : 86400,
    "month"     : 2592000,
    "months"    : 2592000,
}

class remindme:
    """Remind me of stuff"""

    def __init__(self, bot):
        self.bot = bot

        #Check files
        try:
            remindersList = json.load(open("reminders.json"))
        except:
            remindersList = {}
            with open("reminders.json", "w") as outfile:
                json.dump(remindersList, outfile)

    @commands.command(pass_context=True)
    async def remindme(self, ctx, length: int, unit: str, *, text: str):
        """Sends you a reminder. Cannot be shorter than 1 minute"""
        #Check input
        if length < 1:
            await self.bot.say("You must specify a time greater than 0.")
            return
        if unit.lower() not in timeConversions:
            await self.bot.say("You must specify minute(s)/hour(s)/day(s)/month(s).")
            return
        if len(text) > 1000:
            await self.bot.say("Reminder text is too long.")
            return

        #Calculate the time at which the bot should remind the user
        seconds = length * timeConversions[unit]
        currentTime = time.time()
        remindTime = currentTime + seconds

        #Get the user and channel ID
        userID = ctx.message.author.id
        channelID = ctx.message.channel.id

        #Save the reminder
        remindersList = json.load(open("reminders.json"))
        remindersList[remindTime] = [text, userID, channelID]

        with open("reminders.json", "w") as outfile:
            json.dump(remindersList, outfile)

        await self.bot.say("I'll remind you '{}' in {} {}".format(text, length, unit))

    async def check_reminders(self):
        """Check Reminders"""
        while not self.bot.is_closed:
            remindersList = json.load(open("reminders.json"))
            if len(remindersList) > 0:
                tempDictionary = dict(remindersList)
                for reminder in remindersList:
                    temp = float(reminder)
                    if temp < time.time():
                        reminderText = remindersList[reminder][0]
                        userID = remindersList[reminder][1]
                        channelID = remindersList[reminder][2]
                        reminderMessage = "<@{}> {}".format(userID, reminderText)
                        await self.bot.send_message(self.bot.get_channel(channelID), reminderMessage)
                        del tempDictionary[reminder]
                with open("reminders.json", "w") as outfile:
                    json.dump(tempDictionary, outfile)
            await asyncio.sleep(5)

def setup(bot):
    loop = asyncio.get_event_loop()
    loop.create_task(remindme(bot).check_reminders())
    bot.add_cog(remindme(bot))
