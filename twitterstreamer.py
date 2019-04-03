import json
import logging
import os

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import api

from tweepy.models import Status

logger = logging.getLogger(__name__)

consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

followingList = json.load(open("followinglist.json"))

class TwitterStreamer(StreamListener):
    def on_status(self, status):
        #Ensure that from the tweet we recieve, that the user is actually on the following list
        if status.user.screen_name.lower() in followingList:
            #Construct the URL for the tweet
            tweetURL = "https://twitter.com/{}/status/{}".format(status.user.screen_name, status.id)

            #Save the tweet to json along with the screen name so we can identify information for posting the tweet to the correct channel
            try:
                tweets = json.load(open("tweets.json"))
                tweets[status.id] = [status.user.screen_name.lower(), tweetURL]
                with open("tweets.json", "w") as outfile:
                    json.dump(tweets, outfile)
            except:
                tweets = {}
                tweets[status.id] = [status.user.screen_name.lower(), tweetURL]
                with open("tweets.json", "w") as outfile:
                    json.dump(tweets, outfile)

        return True

    def on_error(self, code):
        logging.error("{}: {}".format(code, errorCodes(code)))
        #Twitter error 420 means that the app is being rate limited
        #Consecutive 420 error codes will increase the length of time that the client must wait
        if code == 420:
            return False

def FollowUser(username: str, channelID: int):
    try:
        stream.disconnect()
        twitterID = ConvertUsernameToID(username)

        if twitterID is None:
            return "Cannot find the user: {}".format(username)

        followingList[username.lower()] = [twitterID, channelID]
        with open("followinglist.json", "w") as outfile:
            json.dump(followingList, outfile)

        idList = ""
        for i in followingList:
            idList += str(followingList[i][0])
            idList += ", "

        stream.filter(follow=[idList], is_async=True)
        return "Started following {}".format(username)
    except Exception as e:
        logging.error(str(e))
        return str(e)

def UnfollowUser(username: str):
    try:
        if username not in followingList:
            return "You are not following {}".format(username)

        stream.disconnect()

        tempList = followingList
        del tempList[username]

        with open("followinglist.json", "w") as outfile:
            json.dump(tempList, outfile)

        idList = ""
        for i in followingList:
            idList += str(followingList[i][0])
            idList += ", "

        stream.filter(follow=[idList], is_async=True)
        return "Unfollowed {}".format(username)
    except Exception as e:
        logging.error(str(e))
        return str(e)

def ConvertUsernameToID(username: str):
    user = api.get_user(screen_name=username)
    return user.id


idList = ""
for i in followingList:
    idList += str(followingList[i][0]) + ", "

l = TwitterStreamer()

stream = Stream(auth, l)
stream.filter(follow=[idList], is_async=True)

#https://developer.twitter.com/en/docs/basics/response-codes.html
def errorCodes(x):
    return {
        400:"Bad Request - The request was invalid or cannot be otherwise served.",
        401:"Unauthorized - Missing or incorrect authentication credentials.",
        403:"Forbidden - The request is understood, but it has been refused or access is not allowed.",
        404:"Not Found - The URI requested is invalid or the resource requested, such as a user, does not exist.",
        406:"Not Acceptable - Returned when an invalid format is specified in the request.",
        410:"Gone - This resource is gone. Used to indicate that an API endpoint has been turned off.",
        420:"Enhance Your Calm - Returned when an app is being rate limited for making too many requests.",
        422:"Unprocessable Entity - Returned when the data is unable to be processed.",
        429:"Too Many Requests - Returned when a request cannot be served due to the app's rate limit having been exhausted for the resource.",
        500:"Internal Server Error - Something is broken. This is usually a temporary error, for example in a high load situation or if an endpoint is temporarily having issues.",
        502:"Bad Gateway - Twitter is down, or being upgraded.",
        503:"Service Unavailable - The Twitter servers are up, but overloaded with requests. Try again later.",
        504:"Gateway timeout - The Twitter servers are up, but the request couldn’t be serviced due to some failure within the internal stack. Try again later."
    }[x]
