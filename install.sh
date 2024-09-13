#!/bin/bash

# Step 1: Update and Install Dependencies
echo "Updating package lists..."
sudo apt-get update -y

echo "Installing required packages..."
sudo apt-get install -y python3 python3-pip

# Step 2: Install the Required Python Packages
echo "Installing Python packages..."
pip3 install python-telegram-bot==20.0

# Step 3: Download the Bot Script
echo "Downloading the bot script..."
wget -O myria_status_bot.py https://raw.githubusercontent.com/egzakutacno/myria_status/main/myria_status_bot.py

# Step 4: Create a Service to Run the Bot
echo "Creating systemd service file..."
cat <<EOL | sudo tee /etc/systemd/system/myria_bot.service
[Unit]
Description=Myria Status Telegram Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/myria_status_bot.py
WorkingDirectory=/root
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL

# Step 5: Start the Bot as a Service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling the bot service to start on boot..."
sudo systemctl enable myria_bot.service

echo "Starting the bot service..."
sudo systemctl start myria_bot.service

echo "The bot should now be running. Use 'sudo systemctl status myria_bot.service' to check its status."
