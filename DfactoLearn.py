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
    '''
    slackTS = ["nameSlackTS","clientSlackTS", "projectSlackTS", "interestsSlackTS", 
                "hobbysSlackTS", "funFactSlackTS", "agileLevelSkackTS", "agileInterestSlackTS", 
                "javascriptLevelSlackTS", "javascriptInterestSlackTS", "javascriptSlackTS", 
                "pythonLevelSlackTS", "pythonInterestSlackTS"]
    '''
    slackTS = [{"type": "name", "ts": user["name"]["ts"]}, 
                {"type": "client", "ts": user["client"]["ts"]}, 
                {"type": "project", "ts": user["project"]["ts"]},
                {"type": "interests", "ts": user["interests"]["ts"]},
                {"type": "hobbys", "ts": user["hobbys"]["ts"]},
                {"type": "funFacts", "ts": user["funFacts"]["ts"]}]
    slackTS += [{"type": "interest", "ts": user["skills"][skillLevel]["level"]["ts"]} for skillLevel in user["skills"]]
    slackTS += [{"type": "interest", "ts": user["skills"][skillInterest]["interest"]["ts"]} for skillInterest in user["skills"]]
    print(slackTS)
    for ts in slackTS:
        if(ts["ts"] != ""):
            replyData = slack.api_call("im.replies", channel=user["slack"]["channel"], thread_ts=ts["ts"])
            for reply in replyData["messages"]:
                if(reply["user"] == user["slack"]["user"]):
                    slackTSReply = reply["text"]
                    if(ts["type"] in ("name", "client", "project", "interests", "hobbys")):
                        mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {ts["type"]: {ts["type"]: slackTSReply}}})
                    else:
                        mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {"skills": {ts["type"]: {ts["type"]: slackTSReply}}}})
    '''
    for ts in slackTS:
        if(user[ts] != "" and user[ts.replace("SlackTS", "")] == ""):
            replyData = slack.api_call("im.replies", channel=user["slackChannel"], thread_ts=user[ts])
            for reply in replyData["messages"]:
                if(reply["user"] == user["slackUsername"]):
                    slackTSReply = reply["text"]
                    mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {ts.replace("SlackTS", ""): slackTSReply}})
    '''


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