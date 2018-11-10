###################
##### Imports #####
###################
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient
from bson import ObjectId
from Dfacto import messageSlack


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")


##########################
##### Ask a Question #####
##########################
def askAQuestion(user):
    question = "*Daily Question*\n"
    # Check if we have a name
    if(user["name"] == ""):
        question += "_What is your name (first and last)?_"
        slackTS = "nameSlackTS"
    # Check if have a client
    elif(user["client"] == ""):
        question += "_What engagement are you currently at?_"
        slackTS = "clientSlackTS"
    # Check if we have a project
    elif(user["project"] == ""):
        question += "_What projet are you currently working on?_"
        slackTS = "projectSlackTS"
    # Start running through skills
    else:
        for skill in ("agileLevel", "agileInterest", "javascriptLevel", 
                        "javascriptInterest", "pythonLevel", "pythonInterest"):
            if(user[skill] == ""):
                if("Level" in skill):
                    question += "_On a scale of 0-10, how well do you know {skill}?_".format(skill=skill.replace("Level", ""))
                else:
                    question += "_On a scale of 0-10, how much interest do you have in {skill}_".format(skill=skill.replace("Interest", ""))
                slackTS = "{skill}SlackTS".format(skill=skill)
                break
    question += "\nReply to this message's thread with your answer."
    if(question != "*Daily Question*\n\nReply to this message with your answer."):
        # Send the message to the user
        message = messageSlack(client=slack, channel=user["slackChannel"], attachments=[], message=question)
        # Update Mongo
        try:
            mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {slackTS: message["ts"]}})
        except Exception as e:
            print("Error updating Mongo with Slack Message TS: {error}".format(error=e))


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
        askAQuestion(user=userData)