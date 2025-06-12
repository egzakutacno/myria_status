#!/usr/bin/env python3
import subprocess
import time
import requests
import json
import os
from datetime import datetime, timedelta
import pytz
import sys

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file '{CONFIG_FILE}' not found. Please run the installer again.")
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        bot_token = data.get("bot_token")
        chat_id = data.get("chat_id")
        if not bot_token or not chat_id:
            print("Bot token or chat ID missing in config. Please fix your config.")
            sys.exit(1)
        return bot_token, chat_id

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def check_myria_status():
    try:
        result = subprocess.run(
            ["myria-node", "--status"], capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        return output
    except Exception as e:
        return f"Error running myria-node --status: {e}"

def is_node_online(output):
    return (
        ">>>[INFO] Current Cycle Status: running" in output
        and ">>>[INFO] Myria Node Service is running!" in output
    )

def get_next_run_times(timezone):
    now = datetime.now(timezone)
    today_8_20 = now.replace(hour=8, minute=20, second=0, microsecond=0)
    today_15_20 = now.replace(hour=15, minute=20, second=0, microsecond=0)
    if now > today_15_20:
        # next run is tomorrow 8:20
        next_8_20 = today_8_20 + timedelta(days=1)
        next_15_20 = today_15_20 + timedelta(days=1)
    elif now > today_8_20:
        next_8_20 = today_8_20 + timedelta(days=1)
        next_15_20 = today_15_20
    else:
        next_8_20 = today_8_20
        next_15_20 = today_15_20
    return next_8_20, next_15_20

def main():
    bot_token, chat_id = load_config()
    timezone = pytz.timezone("Asia/Hong_Kong")

    send_telegram_message(bot_token, chat_id, "Myria Monitor started.")

    # Run initial check immediately
    output = check_myria_status()
    if is_node_online(output):
        print("Node is online on start.")
    else:
        send_telegram_message(bot_token, chat_id, f"NODE IS OFFLINE on start:\n{output}")

    # Track last alert to avoid spamming
    last_alert_sent = False

    while True:
        now = datetime.now(timezone)
        # Wait until next scheduled times (8:20 and 15:20 HK time)
        next_8_20, next_15_20 = get_next_run_times(timezone)
        # Find the closest next run
        next_run = min(next_8_20, next_15_20)

        # Sleep until next_run, checking every 10 seconds to handle shutdown
        while datetime.now(timezone) < next_run:
            time.sleep(10)

        # Run the status check
        output = check_myria_status()

        if is_node_online(output):
            print(f"{datetime.now(timezone)}: Node is online.")
            last_alert_sent = False
        else:
            if not last_alert_sent:
                send_telegram_message(bot_token, chat_id, f"NODE IS OFFLINE:\n{output}")
                last_alert_sent = True
            else:
                print(f"{datetime.now(timezone)}: Node offline alert already sent.")

        # Sleep 60 seconds after check to avoid double run
        time.sleep(60)


if __name__ == "__main__":
    main()
