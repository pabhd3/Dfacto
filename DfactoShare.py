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
    users = []
    for user in mongoDB.users.find():
        if(user["client"] != "" or user["project"] != "" or
                user["interests"] != "" or user["hobbys"] != "" or user["funFact"] != "" or
                user["agileLevel"] != "" or user["agileInterest"] != "" or
                user["javascriptLevel"] != "" or user["javascriptInterest"] != "" or
                user["pythonLevel"] != "" or user["pythonInterest"] != ""):
            users.append(user)
    print(len(users))