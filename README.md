# art-alert

A basic discord bot to alert when new images, videos, and gifs are posted in a forum (or normal chat). It sends alerts to a different chat and includes a link to view the original post. It also adds an emoji reaction if you add that to the env.

Originally created by [devinyems156](https://www.fiverr.com/devinyems156) on Fiverr

Modified by me (thatbluflame) for fun

# How to use


Configure '.env.example' with your discord bot token, and rename to '.env'

**OPTIONAL: change EMOJI_ID (within .env.example) to the id of the emoji you want to use for an automatic reaction to each alert, either use the actual emoji if its a unicode emoji or find the id using backslash \ and then ur emote, like \:pallas: and it should give you your emoji id**

I recommend using python 3.10 cuz thats what im using and im not sure if the other versions break anything.

# How to Run: 


pip install -r requirements.txt


python3 main.py


# How to Use:

The bot should create slash commands upon joining a server, you can generate an invite link [here](https://discordapi.com/permissions.html), just be sure to give the bot the correct intents to read messages. 

/setlogchannel: sets the channel to report new art too

/setsourcechannel: sets the channel(s) to find art

/listchannels: lists channels that are in use

/hello: checks if the bot is online

# How to use as a service (debian)


Edit it and change the working directory to wherever you put the bot, and rename to 'artalert.service'


Put 'artalert.service' into '/etc/systemd/system'


Run with: 


systemctl enable artalert


systemctl start artalert

# Personally though, I use [PM2](https://pm2.keymetrics.io/docs/usage/quick-start/), way easier to use than a service.
