###################
##### Imports #####
###################
from time import sleep
from os import environ
from slackclient import SlackClient


############################
##### Global Variables #####
############################
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_ID = environ.get("BOT_ID")


if __name__ == "__main__":
    # Instantiate Slack Connection
    slack = SlackClient(SLACK_BOT_TOKEN)
    READ_WEBSOCKET_DELAY = 1
    try:
        if(slack.rtm_connect()):
            print("Successfully connected to Slack!")
            while(True):
                slackFeed = slack.rtm_read()
                sleep(READ_WEBSOCKET_DELAY)
    except Exception as e:
        print("Fatar Error: {error}".format(error=e))