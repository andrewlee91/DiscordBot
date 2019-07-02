# Discord-Bot
[![Build Status](https://travis-ci.com/andrewlee91/Discord-Bot.svg?branch=master)](https://travis-ci.com/andrewlee91/Discord-Bot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A Discord bot made in Python using discord.py. 

requirements.txt is generated using [pipreqs](https://github.com/bndr/pipreqs).

## To-Do
A non exhaustive list of features or functionality that I'd like to add some time in the future.
- Search
  - YouTube
  - Reddit
  - Imgur
- Overwatch/Fortnite/Apex/etc stats lookup
- YouTube notifications
- TwitchTV notifications
- Warframe notifications
- Polls
- Suggestions with Trello integration
- Trivia
- Music (I'll probably seperate this to a different bot if it gets too big)
- Moderation tools including blacklist
- Support for multiple servers
- General clean up and restructuring 

## Issues
- An apparent websockets bug can cause the following issue. This may explain issues with Twitter streaming but it does not interfere with any other aspect of the bot.

    ```
    13-Apr-19 00:32:49 - Shard ID None has stopped responding to the gateway. Closing and restarting.
    13-Apr-19 00:54:21 - Can't keep up, websocket is 13.5s behind.
    ```
