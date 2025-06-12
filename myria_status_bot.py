import subprocess
import requests
import time
import json
import os

CONFIG_FILE = '/opt/myria-monitor/config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config['bot_token'], config['chat_id']
    else:
        bot_token = input("Enter your Telegram bot token: ").strip()
        chat_id = input("Enter your Telegram chat ID: ").strip()
        save_config(bot_token, chat_id)
        return bot_token, chat_id

def save_config(bot_token, chat_id):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'bot_token': bot_token, 'chat_id': chat_id}, file)

def send_telegram_message(bot_token, chat_id, message):
    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(telegram_api_url, data=payload)
        if not response.ok:
            print(f"Failed to send message: {response.text}")
        return response.ok
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False

def check_node_status(bot_token, chat_id):
    try:
        result = subprocess.run(
            ['myria-node', '--status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout
        if "Current Cycle Status: running" in output and "Myria Node Service is running!" in output:
            print("✅ Myria Node is healthy.")
            return True
        else:
            send_telegram_message(bot_token, chat_id, "⚠️ Myria Node is NOT healthy on this VM.\nStatus output:\n" + output)
            return False
    except subprocess.TimeoutExpired:
        send_telegram_message(bot_token, chat_id, "⏱️ Myria Node status check timed out on this VM.")
        return False
    except Exception as e:
        send_telegram_message(bot_token, chat_id, f"❌ Error checking Myria Node status on this VM:\n{e}")
        return False

def main():
    bot_token, chat_id = load_config()

    while True:
        check_node_status(bot_token, chat_id)
        time.sleep(3600)  # Check every hour, adjust if needed

if __name__ == "__main__":
    main()
