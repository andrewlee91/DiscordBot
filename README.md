# DiscordBot
A Discord bot made in Python using discord.py. It is not intended to manage multiple servers at once just yet. Requirements.txt is generated using [pipreqs](https://github.com/bndr/pipreqs).

## Requirements
- Python 3.6.7
- [discord.py 1.0.0](https://github.com/Rapptz/discord.py)
- [tweepy 3.7.0](https://github.com/tweepy/tweepy)
- [requests 2.21.0](https://github.com/kennethreitz/requests)

## Issues
- An apparent websockets bug can cause the following issue. This may explain issues with Twitter streaming but it does not interfere with any other aspect of the bot.

    ```
    13-Apr-19 00:32:49 - Shard ID None has stopped responding to the gateway. Closing and restarting.
    13-Apr-19 00:54:21 - Can't keep up, websocket is 13.5s behind.
    ```
