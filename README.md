# Dfacto
Daugherty Hack-a-thon Fall 2018

The purpose of this Slackbot is to gather and distribute information from willing participants in order to expand everyone's knowledgebase.

---

## How to Use

* **(Optional) Set up a Virtual Environment**

    $ virtualenv ENV

    $ source ENV/bin/activate

    (ENV) $ ENV/bin/pip3 install -r requirements.txt

- Note that you'll need to pip3 install the requirements regardless of whether you do it in a virtual environment or not.
- Also note, if you chose to set up a virtual environment, you will need to replace instances of `python3` with `ENV/bin/python3` in the following sections.

* **Set-up Environment Variables**

- You'll need to set up several environment variables, including: 

    `SLACK_BOT_TOKEN`: Used to connect to Slack & Slack RTM

    `BOT_ID`: Used to determine if a message was directed at the bot, via `@Dfacto`.

    `Dfacto_Example_Site`: Used as an example fact page for given users (currently non-functional).

* **Starting the Bot**

    $ python3 Dfacto.py

- This script will start the Slackbot, connect to Mongo and Slack RTM, and continuously read off the RTM Stream.

    $ python3 DfactoAsk.py

- This script will send a question to all users who have opted in to the bot.

    $ python3 DfactoLearn.py

- This script will gather the in-thread replys to the questions asked in `DfactoAsk.py`.

    $ python3 DfactoShare.py

- This script will share facts learned from `DfactoLearn.py` between those who are eligible to share facts.

## **Demo Mode**

    $ python3 demo.py

- This script will connect to MongoDB and leave it running in the background, start the `Dfacto.py` script and leave it running in the background, then continuously run the `DfactoAsk.py`, `DfactoLearn.py` and `DfactoShare.py` scripts.
- Note that on Line 8, you may need to comment/alter the line depending on how your MongoDB is set up.
