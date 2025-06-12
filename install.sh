#!/bin/bash

# Simple installer for Myria Node Monitor

echo "Installing Python and requests if not already installed..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install requests

echo "Please enter your Telegram bot token:"
read BOT_TOKEN
echo "Please enter your Telegram chat ID:"
read CHAT_ID

echo "Copying the monitoring script to /opt/myria-monitor..."
sudo mkdir -p /opt/myria-monitor
sudo cp myria_status_bot.py /opt/myria-monitor/

echo "Saving configuration..."
echo "{\"bot_token\": \"$BOT_TOKEN\", \"chat_id\": \"$CHAT_ID\"}" | sudo tee /opt/myria-monitor/config.json > /dev/null

echo "Creating systemd service..."
cat <<EOT | sudo tee /etc/systemd/system/myria-monitor.service
[Unit]
Description=Myria Node Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/myria-monitor/myria_status_bot.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOT

echo "Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable myria-monitor.service
sudo systemctl start myria-monitor.service

echo "✅ Installation complete! The Myria Monitor is now running in the background."
echo "You can check its status with: sudo systemctl status myria-monitor"
