#! /bin/sh

# uninstall systemd service and timer
sudo systemctl disable raptus-discordbot.timer
sudo systemctl stop raptus-discordbot.timer

sudo rm /etc/systemd/system/raptus-discordbot.service
sudo rm /etc/systemd/system/raptus-discordbot.timer

sudo systemctl daemon-reload
