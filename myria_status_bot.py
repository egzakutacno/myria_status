import subprocess
import requests
import os
import time
import json
import sys
import threading

# Set this variable for your bot token
BOT_TOKEN = "6613010335:AAEmKD0XI9CcJFBHfnAy0Tpp4VuYGDV4ssM"

# Path to store the chat ID, VPS identifier, and interval (local JSON file)
CONFIG_FILE = "vps_config.json"

# Function to get the stored config, or prompt the user
def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config
    else:
        chat_id = input("Please enter your Telegram chat ID: ")
        vps_identifier = os.uname()[1]  # Using hostname as unique VPS identifier
        interval = input("How often (in hours) would you like to check the status of your nodes? ")
        config = {"chat_id": chat_id, "vps_identifier": vps_identifier, "interval": int(interval)}
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

# Function to send VPS status at user-defined intervals
def send_status_periodically():
    config = get_config()
    interval_hours = config["interval"]
    
    while True:
        status = get_myria_node_status()
        message = f"VPS: {config['vps_identifier']}\n\nStatus:\n{status}"
        send_telegram_message(config["chat_id"], message)
        
        print(f"Status sent to {config['chat_id']}. Next update in {interval_hours} hours.")
        time.sleep(interval_hours * 60 * 60)  # Sleep for the user-defined number of hours

# Function to automatically register VPS with your bot
def register_vps_with_bot():
    config = get_config()
    message = f"Auto-registration: VPS {config['vps_identifier']} has been registered."
    send_telegram_message(config["chat_id"], message)

# Function to restart the script in the background using nohup
def restart_in_background():
    print("Restarting the script in the background...")
    subprocess.Popen(['nohup', 'python3', sys.argv[0], '&'], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    print("Script is now running in the background.")
    sys.exit()  # Exit the current foreground process

# Function to check incoming Telegram messages
def listen_for_commands():
    config = get_config()
    chat_id = config["chat_id"]
    last_update_id = None

    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if last_update_id:
            url += f"?offset={last_update_id + 1}"
        
        response = requests.get(url).json()

        if response["ok"]:
            for result in response["result"]:
                update_id = result["update_id"]
                message = result.get("message")
                
                if message:
                    text = message.get("text")
                    sender_chat_id = message.get("chat", {}).get("id")
                    
                    # Check if the sender's chat ID matches the stored chat ID
                    if sender_chat_id == int(chat_id):
                        if text == "/status":
                            status = get_myria_node_status()
                            response_message = f"VPS: {config['vps_identifier']}\n\nStatus:\n{status}"
                            send_telegram_message(chat_id, response_message)

                last_update_id = update_id

        time.sleep(2)  # Poll every 2 seconds

# Main function
def main():
    # Automatically register VPS on first run
    register_vps_with_bot()

    # Check if already running with nohup
    if 'NOHUP_RUNNING' not in os.environ:
        # Restart the script with nohup
        os.environ['NOHUP_RUNNING'] = '1'  # Set an environment variable to avoid infinite loop
        restart_in_background()

    # Start listening for /status command in a separate thread
    command_listener_thread = threading.Thread(target=listen_for_commands)
    command_listener_thread.daemon = True
    command_listener_thread.start()

    # Start the interval status sending
    send_status_periodically()

if __name__ == "__main__":
    main()
