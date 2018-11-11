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


###################################
##### Send a Message to Slack #####
###################################
def messageSlack(client, channel, attachments, message):
    try:
        message = client.api_call("chat.postMessage", channel=channel, attachments=attachments, text=message, as_user=True)
        return message
    except Exception as e:
        print("Error send Slack Message: {error}".format(error=e))
        

##########################
##### Ask a Question #####
##########################
'''
def askAQuestion(user):
    question = "*Daily Question*\n"
    # Check if we have a name
    if(user["name"]["name"] == ""):
        question += "_What is your name (first and last)?_"
        slackTS = "name"
    # Check if have a client
    elif(user["client"]["client"] == ""):
        question += "_What engagement are you currently at?_"
        slackTS = "client"
    # Check if we have a project
    elif(user["project"]["project"] == ""):
        question += "_What projet are you currently working on?_"
        slackTS = "project"
    # Check if we have a interests
    elif(user["interests"]["interests"] == ""):
        question += "_What interests do you have?_"
        slackTS = "interests"
    # Check if we have a hobbys
    elif(user["hobbys"]["hobbys"] == ""):
        question += "_What hobbys do you have?_"
        slackTS = "hobbys"
    # Check if we have a fun facts
    # elif(user["funFacts"]["funFacts"] == ""):
    #     question += "_What are some fun facts about you?_"
    #     slackTS = "funFacts"
    # Start running through skills
    else:
        foundBlank = False
        for skill in user["skills"]:
            print(skill)
            for levelInterest in user["skills"][skill]:
                print(levelInterest)
                if(levelInterest == "level"):
                    print('user["skills"][skill]["level"]', user["skills"][skill]["level"])
                    if(user["skills"][skill]["level"]["level"] == ""):
                        print("BLANK LEVEL")
                        question += "_On a scale of 0-10, how well do you know {skill}?_".format(skill=skill.replace("Level", ""))
                        slackTS = {"skill": skill, "type": "level"}
                        foundBlank = True
                else:
                    print('user["skills"][skill]["interest"]', user["skills"][skill]["interest"])
                    if(user["skills"][skill]["interest"]["interest"] == ""):
                        print("BLANK INTEREST")
                        question += "_On a scale of 0-10, how much interest do you have in {skill}_".format(skill=skill.replace("Interest", ""))
                        slackTS = {"skill": skill, "type": "interest"}
                        foundBlank = True
                if(foundBlank):
                    break
            if(foundBlank):
                break
    question += "\nReply to this message's thread with your answer."
    if(question != "*Daily Question*\n\nReply to this message with your answer."):
        # Send the message to the user
        message = messageSlack(client=slack, channel=user["slack"]["channel"], attachments=[], message=question)
        #message = messageSlack(client=slack, channel=user["slackChannel"], attachments=[], message=question)
        # Update Mongo
        try:
            if(slackTS in ("name", "client", "project", "interests", "hobbys", "funFacts")):
                mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {slackTS: {"ts": message["ts"]}}})
            else:
                mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {"skills": {slackTS["skill"]: {slackTS["type"]: {"ts": message["ts"]}}}}})
            # mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {slackTS: message["ts"]}})
        except Exception as e:
            print("Error updating Mongo with Slack Message TS: {error}".format(error=e))
'''
##########################
##### Ask a Question #####
##########################
def askAQuestion(client, mongoDB, user):
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
        question += "_What project are you currently working on?_"
        slackTS = "projectSlackTS"
    # Check if we have interests
    elif(user["interests"] == ""):
        question += "_What are your interests?_"
        slackTS = "interestsSlackTS"
    # Check if we have hobbys
    elif(user["hobbys"] == ""):
        question += "_What are your hobbys?_"
        slackTS = "hobbysSlackTS"
    # Check if we have fun facts
    elif(user["funFact"] == ""):
        question += "_What are some fun facts about you?_"
        slackTS = "funFactSlackTS"
    # Start running through skills
    else:
        foundBlank = False
        for skill in ("agileLevel", "agileInterest", "javascriptLevel", 
                        "javascriptInterest", "pythonLevel", "pythonInterest"):
            if(user[skill] == ""):
                if("Level" in skill):
                    question += "_On a scale of 0-10, how well do you know {skill}?_".format(skill=skill.replace("Level", ""))
                else:
                    question += "_On a scale of 0-10, how much interest do you have in {skill}_".format(skill=skill.replace("Interest", ""))
                slackTS = "{skill}SlackTS".format(skill=skill)
                foundBlank = True
            if(foundBlank):
                break
    question += "\nReply to this message's thread with your answer."
    try:
        if(slackTS):
            # Send the message to the user
            message = messageSlack(client=client, channel=user["slackChannel"], attachments=[], message=question)
            # Update Mongo
            try:
                mongoDB.users.update_one({"_id": user["_id"]}, {"$set": {slackTS: message["ts"]}})
            except Exception as e:
                print("Error updating Mongo with Slack Message TS: {error}".format(error=e))
    except Exception as e:
        print("askAQuestion() Error: {error}".format(error=e))
        pass


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
        askAQuestion(client=slack, mongoDB=mongoDB, user=userData)