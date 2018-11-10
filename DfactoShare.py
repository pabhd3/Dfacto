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
    for userData in mongoDB.users.find():
        print(userData)