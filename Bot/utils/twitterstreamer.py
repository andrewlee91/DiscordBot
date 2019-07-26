import json
import logging
import os

import tweepy
from tweepy import OAuthHandler, Stream, api
from tweepy.models import Status
from tweepy.streaming import StreamListener

logger = logging.getLogger(__name__)

data_directory = "{}/Bot/data".format(os.getcwd())
tweets_path = "{}/tweets.json".format(data_directory)
followinglist_path = "{}/followinglist.json".format(data_directory)


class TwitterStreamer(StreamListener):
    def on_status(self, status):
        # Ensure that from the tweet we recieve, that the user is actually on the following list
        if status.user.screen_name.lower() in followingList:
            # Get JSON for the status because it's easier to parse
            statusJSON = status._json

            # Ensure it's not a retweet or reply to another user
            if "retweeted_status" not in statusJSON and (
                statusJSON["in_reply_to_user_id"] is None
                or statusJSON["in_reply_to_screen_name"]
                == statusJSON["user"]["screen_name"]
            ):
                # Construct the URL for the tweet
                tweetURL = "https://twitter.com/{}/status/{}".format(
                    statusJSON["user"]["screen_name"], statusJSON["id"]
                )

                # Save the tweet to json along with the screen name so we can identify information for posting the tweet to the correct channel
                try:
                    tweets = json.load(open(tweets_path))
                    tweets[status.id] = [status.user.screen_name.lower(), tweetURL]
                    with open(tweets_path, "w") as outfile:
                        json.dump(tweets, outfile)
                except:
                    tweets = {}
                    tweets[status.id] = [status.user.screen_name.lower(), tweetURL]
                    with open(tweets_path, "w") as outfile:
                        json.dump(tweets, outfile)

        return True

    def on_error(self, code):
        logging.error("{}: {}".format(code, errorCodes(code)))
        # Twitter error 420 means that the app is being rate limited
        # Consecutive 420 error codes will increase the length of time that the client must wait
        if code == 420:
            return False


consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

followingList = {}

l = TwitterStreamer()
stream = Stream(auth, l)


def Setup_Files():
    if not os.path.isdir(data_directory):
        os.makedirs(data_directory)

    if os.path.isfile(followinglist_path):
        followingList = json.load(open(followinglist_path))
    else:
        followingList = {}
        with open(followinglist_path, "w") as outfile:
            json.dump(followingList, outfile)

    if os.path.isfile(tweets_path):
        tweets = json.load(open(tweets_path))
    else:
        tweets = {}
        with open(tweets_path, "w") as outfile:
            json.dump(tweets, outfile)


def Follow_User(username: str, channelID: int):
    try:
        stream.disconnect()
        twitterID = Convert_Username_To_ID(username)

        if twitterID is None:
            return "Cannot find the user: {}".format(username)

        followingList[username.lower()] = [twitterID, channelID]
        with open(followinglist_path, "w") as outfile:
            json.dump(followingList, outfile)

        Start_Streamer()
        return "Started following {}".format(username)
    except Exception as e:
        logging.error(str(e))
        return str(e)


def Unfollow_User(username: str):
    try:
        if username not in followingList:
            return "You are not following {}".format(username)

        stream.disconnect()

        tempList = followingList
        del tempList[username]

        with open(followinglist_path, "w") as outfile:
            json.dump(tempList, outfile)

        Start_Streamer()
        return "Unfollowed {}".format(username)
    except Exception as e:
        logging.error(str(e))
        return str(e)


def Convert_Username_To_ID(username: str):
    user = api.get_user(screen_name=username)
    return user.id


def Start_Streamer():
    if not followingList:
        print("Following list is empty")
    else:
        idList = ""
        for i in followingList:
            idList += str(followingList[i][0]) + ", "

        stream.filter(follow=[idList], is_async=True)


# https://developer.twitter.com/en/docs/basics/response-codes.html
def errorCodes(x):
    return {
        400: "Bad Request - The request was invalid or cannot be otherwise served.",
        401: "Unauthorized - Missing or incorrect authentication credentials.",
        403: "Forbidden - The request is understood, but it has been refused or access is not allowed.",
        404: "Not Found - The URI requested is invalid or the resource requested, such as a user, does not exist.",
        406: "Not Acceptable - Returned when an invalid format is specified in the request.",
        410: "Gone - This resource is gone. Used to indicate that an API endpoint has been turned off.",
        420: "Enhance Your Calm - Returned when an app is being rate limited for making too many requests.",
        422: "Unprocessable Entity - Returned when the data is unable to be processed.",
        429: "Too Many Requests - Returned when a request cannot be served due to the app's rate limit having been exhausted for the resource.",
        500: "Internal Server Error - Something is broken. This is usually a temporary error, for example in a high load situation or if an endpoint is temporarily having issues.",
        502: "Bad Gateway - Twitter is down, or being upgraded.",
        503: "Service Unavailable - The Twitter servers are up, but overloaded with requests. Try again later.",
        504: "Gateway timeout - The Twitter servers are up, but the request couldn’t be serviced due to some failure within the internal stack. Try again later.",
    }[x]
