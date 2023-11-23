# art-alert
A basic discord bot to alert when new images are posted in a forum.
Originally created by https://www.fiverr.com/devinyems156 on Fiverr
Modified by me (thatbluflame) for fun
How to use
Configure '.env.example' with your discord bot token, and rename to '.env'
How to Run: 
pip install -r requirements.txt
python3 main.py

How to use as a service (debian)
Edit it and change the working directory to wherever you put the bot, and rename to 'artalert.service'
Put 'artalert.service' into '/etc/systemd/system'
Run with: 
systemctl enable artalert
systemctl start artalert
