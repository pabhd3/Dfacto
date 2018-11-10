###################
##### Imports #####
###################
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient
from bson import ObjectId


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_ID = environ.get("BOT_ID")


############################
##### Retrieve Replies #####
############################
def retrieveReplies(user):
    slackTS = ["nameSlackTS","clientSlackTS", "projectSlackTS", "interestsSlackTS", 
                "hobbysSlackTS", "funFactSlackTS", "agileLevelSkackTS", "agileInterestSlackTS", 
                "javascriptLevelSlackTS", "javascriptInterestSlackTS", "javascriptSlackTS", 
                "pythonLevelSlackTS", "pythonInterestSlackTS"]
    for ts in slackTS:
        if(user[ts] != "" and user[ts.replace("SlackTS", "")] == ""):
            replyData = slack.api_call("im.replies", channel=user["slackChannel"], thread_ts=user[ts])
            for reply in replyData["messages"]:
                if(reply["user"] == user["slackUsername"]):
                    slackTSReply = reply["text"]
                    mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {ts.replace("SlackTS", ""): slackTSReply}})


if __name__ == "__main__":
    # Instantiate Slack Connection
    slack = SlackClient(SLACK_BOT_TOKEN)
    print("Successfully connected to Slack!")
    # Instantiate Mongo Connection
    mongo = MongoClient("localhost", 27017)
    mongoDB = mongo.USERS
    print("Successfully connected to Mongo!")
    # Pull list of users
    for userData in mongoDB.users.find():
        retrieveReplies(user=userData)