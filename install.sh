#!/bin/bash

# Update package list and install necessary dependencies
echo "Updating package list..."
sudo apt-get update
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip

# Install Python dependencies from requirements.txt in your GitHub repository
echo "Installing Python dependencies..."
pip3 install -r https://raw.githubusercontent.com/egzakutacno/myria_status/main/requirements.txt

# Download the Python script from your GitHub repository
echo "Downloading the Python script..."
curl -O https://raw.githubusercontent.com/egzakutacno/myria_status/main/myria_status_bot.py

# Make the Python script executable
echo "Making the Python script executable..."
chmod +x myria_status_bot.py



# Notify the user that the script is running in the background
echo "The Python script is now running in the background. Logs are being saved to myria_status.log."
