import subprocess
import requests
import os
import time
import json

# Set this variable for your bot token
BOT_TOKEN = "6613010335:AAEmKD0XI9CcJFBHfnAy0Tpp4VuYGDV4ssM"

# Path to store the chat ID, VPS identifier, and interval (local JSON file)
CONFIG_FILE = "vps_config.json"

# Function to get the stored chat ID, VPS identifier, and interval, or prompt the user
def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config
    else:
        chat_id = input("Please enter your Telegram chat ID: ")
        vps_identifier = os.uname()[1]  # Using hostname as unique VPS identifier
        check_interval = int(input("How often (in hours) would you like to check your node and receive updates? "))
        config = {"chat_id": chat_id, "vps_identifier": vps_identifier, "check_interval": check_interval}
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)
        return config

# Function to get VPS status
def get_myria_node_status():
    try:
        result = subprocess.check_output(["myria-node", "--status"], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error fetching status: {e.output}"

# Function to send a message to Telegram
def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response

# Function to send VPS status based on the user's chosen interval
def send_status_periodically():
    while True:
        config = get_config()
        status = get_myria_node_status()
        message = f"VPS: {config['vps_identifier']}\n\nStatus:\n{status}"
        send_telegram_message(config["chat_id"], message)
        
        print(f"Status sent to {config['chat_id']}. Next update in {config['check_interval']} hours.")
        time.sleep(config["check_interval"] * 60 * 60)  # Sleep for the user-defined interval

# Function to automatically register VPS with your bot
def register_vps_with_bot():
    config = get_config()
    message = f"Auto-registration: VPS {config['vps_identifier']} has been registered."
    send_telegram_message(config["chat_id"], message)

# Main function
def main():
    # Automatically register VPS on first run
    register_vps_with_bot()
    
    # Start the interval-based status sending
    send_status_periodically()

if __name__ == "__main__":
    main()
