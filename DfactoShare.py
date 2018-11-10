###################
##### Imports #####
###################
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient
from Dfacto import messageSlack


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_ID = environ.get("BOT_ID")
SLACK_BOT_DIRECT_MESSAGE = "<@{id}>".format(id=SLACK_BOT_ID)
SLACK_AT_HERE = "<@here>"


if __name__ == "__main__":
    # Instantiate Slack Connection
    slack = SlackClient(SLACK_BOT_TOKEN)
    print("Successfully connected to Slack!")
    # Instantiate Mongo Connection
    mongo = MongoClient("localhost", 27017)
    mongoDB = mongo.USERS
    print("Successfully connected to Mongo!")
    # Pull list of users
    users = mongoDB.users.find()
    for userData in users:
        if(userData["client"]["client"] == "" and userData["project"]["project"] == "" and
            userData["interests"]["interests"] and userData["hobbys"]["hobbys"] and
            userData["funFacts"]["funFacts"] and userData["skills"]["agile"]["level"]["level"] and
            userData["skills"]["agile"]["interest"]["interest"] and userData["skills"]["javascript"]["level"]["level"] and
            userData["skills"]["javascript"]["interest"]["interest"] and userData["skills"]["python"]["interest"]["interest"] and
            userData["skills"]["python"]["level"]["level"]):
            users.pop(users.index(userData))