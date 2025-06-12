import subprocess
import requests
import json
import os
import time
import schedule
from datetime import datetime
from pytz import timezone

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        bot_token = input("Enter your Telegram Bot Token: ")
        chat_id = input("Enter your Telegram Chat ID: ")
        config = {'bot_token': bot_token, 'chat_id': chat_id}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return config

def send_telegram_message(token, chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def check_node_status(config, alert_on_offline=True):
    try:
        result = subprocess.check_output(['myria-node', '--status'], text=True)
        if ('>>>[INFO] Current Cycle Status: running' in result and
            '>>>[INFO] Myria Node Service is running!' in result):
            print(f"[{datetime.now()}] Node is running.")
        else:
            if alert_on_offline:
                send_telegram_message(config['bot_token'], config['chat_id'], f"NODE IS OFFLINE\n\n{result}")
    except Exception as e:
        send_telegram_message(config['bot_token'], config['chat_id'], f"NODE IS OFFLINE\n\nError: {e}")

def main():
    config = load_config()
    
    # Initial Check
    check_node_status(config, alert_on_offline=False)
    send_telegram_message(config['bot_token'], config['chat_id'], "Myria Monitor is now running.")

    # Schedule fixed time checks (Hong Kong Time)
    hk = timezone('Asia/Hong_Kong')

    schedule.every().day.at("08:20").do(check_node_status, config)
    schedule.every().day.at("15:20").do(check_node_status, config)

    # Continuous monitoring every 1 minute
    while True:
        now = datetime.now(hk)
        schedule.run_pending()
        check_node_status(config)
        time.sleep(60)

if __name__ == '__main__':
    main()
