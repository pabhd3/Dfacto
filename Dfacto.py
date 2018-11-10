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
SLACK_BOT_DIRECT_MESSAGE = "<@{id}>".format(id=SLACK_BOT_ID)
SLACK_AT_HERE = "<@here>"


####################################
##### Parse Message From Slack #####
####################################
def parseSlackMessageRTM(slackRTM):
    try:
        if slackRTM and len(slackRTM) > 0:
            for output in slackRTM:
                if(output and 'text' in output and SLACK_BOT_DIRECT_MESSAGE in output['text'] and SLACK_AT_HERE not in output['text']):
                    return output['text'].split(SLACK_BOT_DIRECT_MESSAGE)[1].strip(), output['channel'], output['user']
    except Exception as e:
        print("Error (parseSlackMessageRTM): {error}".format(error=e))
    return None, None, None


if __name__ == "__main__":
    # Instantiate Slack Connection
    slack = SlackClient(SLACK_BOT_TOKEN)
    READ_WEBSOCKET_DELAY = 1
    try:
        if(slack.rtm_connect()):
            print("Successfully connected to Slack!")
            while(True):
                command, channel, user = parseSlackMessageRTM(slack.rtm_read())
                sleep(READ_WEBSOCKET_DELAY)
    except Exception as e:
        print("Fatar Error: {error}".format(error=e))