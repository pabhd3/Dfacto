###################
##### Imports #####
###################
from os import environ
from slackclient import SlackClient
from pymongo import MongoClient
from random import choice, randint


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


#############################
##### Generate Pair List#####
#############################
def generatePairs(count):
    remaining = list(range(0, count))
    pairs = []
    while(True):
        if(len(remaining) == 0):
            break
        if(len(remaining) == 1):
            repeat = True
            while(repeat):
                print(list(range(0, count-1)))
                second = choice(list(range(0, count-1)))
                if(second != remaining[0]):
                    repeat = False
            pairs.append((remaining[0], second))
            break
        first = remaining.pop(0)
        repeat = True
        while(repeat):
            second = choice(remaining)
            if(second != first):
                repeat = False
        remaining.pop(remaining.index(second))
        pairs.append((first, second))
    return pairs


#######################
##### Share Facts #####
#######################
def shareFacts(users, pairs):
    facts = ("client", "project", "interests", "hobbys", "funFact", "agileLevel",
                    "agileInterest", "javascriptLevel", "javascriptInterest", "pythonLevel",
                    "pythonInterest")
    for pair in pairs:
        factMessages = []
        for person in pair:
            notFound = True
            while(notFound):
                factChoice = choice(facts)
                if(users[person][factChoice] != ""):
                    notFound = False
                    if(factChoice == "client"):
                        message = "Did you know <@{user}> is at the {client} engagement?".format(user=users[person]["slackUsername"], client=users[person]["client"])
                    if(factChoice == "project"):
                        message = "Did you know <@{user}> is working on the {project} project?".format(user=users[person]["slackUsername"], project=users[person]["project"])
                    if(factChoice == "interests"):
                        message = "Did you know <@{user}> has the following interests: {interests}?".format(user=users[person]["slackUsername"], interests=users[person]["interests"])
                    if(factChoice == "hobbys"):
                        message = "Did you know <@{user}> has the following hobbys: {hobbys}?".format(user=users[person]["slackUsername"], hobbys=users[person]["hobbys"])
                    if(factChoice == "funFact"):
                        message = "Here are some fun acts about <@{user}>: {facts}".format(user=users[person]["slackUsername"], facts=users[person]["funFact"])
                    if("Level" in factChoice):
                        message = "Did you know <@{user}> has a {level}/10 {skill} skill level?".format(user=users[person]["slackUsername"], level=users[person][factChoice], skill=factChoice.replace("Level", ""))
                    if("Interest" in factChoice):
                        message = "Did you know <@{user}> has a {interest}/10 interest in {skill}?".format(user=users[person]["slackUsername"], interest=users[person][factChoice], skill=factChoice.replace("Interest", ""))
            message += "\nFor an example of a site to see more information, click <{link}|here>.".format(link=environ.get("Dfacto_Example_Site"))
            factMessages.append(message)
        messageSlack(client=slack, channel=users[pair[0]]["slackChannel"], attachments=[], message=factMessages[1])
        messageSlack(client=slack, channel=users[pair[1]]["slackChannel"], attachments=[], message=factMessages[0])


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
    pairs = generatePairs(count=len(users))
    shareFacts(users=users, pairs=pairs)