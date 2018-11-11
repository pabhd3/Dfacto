###################
##### Imports #####
###################
from time import sleep
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import models, DfactoAsk


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_ID = environ.get("BOT_ID")
SLACK_BOT_DIRECT_MESSAGE = "<@{id}>".format(id=SLACK_BOT_ID)
SLACK_AT_HERE = "<@here>"


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
##### Handle Commands ####
##########################
def handleMessage(message, channel, user):
    # Default Response
    response = "I'm sorry, I don't understand. Please use the `@Dfacto How do I use you?` command to see how to use me."
    attachments = []
    message = message.lower()
    ##### How to use #####
    if(message == "how do i use you" or message == "how do i use you?"):
        response = "Here are the commands you can use with me: "
        response += "\n    * `@Dfacto opt in` to opt in to the program. You will then daily recieve questions to answer and facts of others who have opt'd in." 
        response += "\n    * `@Dfacto ask me` to recieve a new question. You will not, at this time, recieve repeat questions. Please not you might recieve a repeat question if you request questions too quickly."
    ##### Opt-in/Welcome Message ####
    elif(message == "opt in"):
        # Add user to Mongo
        if(not mongoDB.users.find_one({"slackUsername": user})):
            newUser = models.USER
            newUser["slackUsername"] = user
            newUser["slackChannel"] = channel
            newUser["optIn"] = datetime.strftime(datetime.now(), "%A, %B %d %Y %I:%M:%S.%f %p")
            '''
            newUser = models.USER_V2
            newUser["slack"]["user"] = user
            newUser["slack"]["channel"] = channel
            newUser["slack"]["optIn"] = datetime.strftime(datetime.now(), "%A, %B %d %Y %I:%M:%S.%f %p")
            '''
            try:
                mongoDB.users.insert_one(newUser)
            except Exception as e:
                print("Error adding user to Mongo: {error}".format(error=e))
        response = "Welcome to Dfacto, the personal trivia game from the creative minds at Daugherty Snake Charmers.  Each day you will receive a fun fact about a fellow Daugherty team member.  You will also be able to share information about yourself by answering one or more questions each day. Thank you for joining."
        response += "\nPlease use the `@Dfacto How do I use you?` command to see how to use me."
    ##### Trigger asking a question #####
    elif(message == "ask me"):
        try:
            user = mongoDB.users.find_one({"slackChannel": channel})
            DfactoAsk.askAQuestion(client=slack, user=user)
            response = None
        except:
            response = "I'm sorry, something went wrong."
    ##### Send Message to Slack #####
    if(response):
        message = messageSlack(client=slack, channel=channel, attachments=attachments, message=response)


####################################
##### Parse Message From Slack #####
####################################
def parseSlackMessageRTM(slackRTM):
    try:
        if slackRTM and len(slackRTM) > 0:
            for output in slackRTM:
                # If text exists, '@Dfacto' in text and '@here' not in text
                if(output and 'text' in output and SLACK_BOT_DIRECT_MESSAGE in output['text'] and SLACK_AT_HERE not in output['text']):
                    # Return text minus '@Dfacto', channel and user
                    return output['text'].split(SLACK_BOT_DIRECT_MESSAGE)[1].strip(), output['channel'], output['user']
    except Exception as e:
        print("Error (parseSlackMessageRTM): {error}".format(error=e))
    return None, None, None


if __name__ == "__main__":
    # Instantiate Slack Connection
    slack = SlackClient(SLACK_BOT_TOKEN)
    print("Successfully connected to Slack!")
    # Instantiate Mongo Connection
    mongo = MongoClient("localhost", 27017)
    mongoDB = mongo.USERS
    print("Successfully connected to Mongo!")
    READ_WEBSOCKET_DELAY = 1
    try:
        # Connect to Slack RTM
        if(slack.rtm_connect()):
            print("Successfully connected to Slack RTM!")
            while(True):
                # Parse Slack RTM and Handle Message
                message, channel, user = parseSlackMessageRTM(slack.rtm_read())
                if(message and channel and user):
                    handleMessage(message=message, channel=channel, user=user)
                sleep(READ_WEBSOCKET_DELAY)
    except Exception as e:
        print("Fatar Error: {error}".format(error=e))