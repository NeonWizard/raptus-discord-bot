#!/bin/sh

# pull latest version from github
git pull

# install pip requirements
sudo python3.7 -m pip install -r requirements.txt

# install systemd service and timer
if [ -f /etc/systemd/system/raptus-discordbot.timer ]; then
    sudo systemctl disable raptus-discordbot.timer
    sudo systemctl stop raptus-discordbot.timer
fi
# sudo cp -f ./raptus-discordbot.service /etc/systemd/system/raptus-discordbot.service
eval "echo -e \"`<raptus-discordbot.service`\"" > /etc/systemd/system/raptus-discordbot.service
eval "echo -e \"`<raptus-discordbot.timer`\"" > /etc/systemd/system/raptus-discordbot.timer

sudo systemctl daemon-reload
sudo systemctl enable raptus-discordbot.timer
sudo systemctl start raptus-discordbot.timer
