###################
##### Imports #####
###################
from time import sleep
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_ID = environ.get("BOT_ID")
SLACK_BOT_DIRECT_MESSAGE = "<@{id}>".format(id=SLACK_BOT_ID)
SLACK_AT_HERE = "<@here>"


##########################
##### Handle Commands ####
##########################
def handleMessage(message, channel):
    # Default Response
    response = "I'm sorry, I don't understand. Please use the `@Dfacto How do I use you?` command to see how to use me."
    attachments = []
    message = message.lower()
    ##### Opt-in/Welcome Message ####
    if(message == "opt in"):
        response = "Welcome Message"
    ##### Send Message to Slack #####
    try:
        message = slack.api_call("chat.postMessage", channel=channel, attachments=attachments, text=response, as_user=True)
    except Exception as e:
        print("Error send Slack Message: {error}".format(error=e))


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
    # Instantiate Mongo Connection
    mongo = MongoClient("localhost", 27017)
    print("Successfully connected to Mongo!")
    READ_WEBSOCKET_DELAY = 1
    try:
        # Connect to Slack RTM
        if(slack.rtm_connect()):
            print("Successfully connected to Slack!")
            while(True):
                # Parse Slack RTM and Handle Message
                message, channel, user = parseSlackMessageRTM(slack.rtm_read())
                if(message and channel and user):
                    handleMessage(message=message, channel=channel)
                sleep(READ_WEBSOCKET_DELAY)
    except Exception as e:
        print("Fatar Error: {error}".format(error=e))