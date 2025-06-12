#!/usr/bin/env python3
import subprocess
import time
import json
import os
from datetime import datetime, timedelta
import requests

CONFIG_FILE = os.path.expanduser("~/.myria_monitor_config.json")
CHECK_TIMES = [("08:20"), ("15:20")]  # HK Time

def get_hk_time():
    # HK timezone is UTC+8, convert current UTC to HK time
    return datetime.utcnow() + timedelta(hours=8)

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        resp = requests.post(url, data=payload, timeout=10)
        if not resp.ok:
            print(f"Failed to send message: {resp.text}")
    except Exception as e:
        print(f"Exception sending Telegram message: {e}")

def run_myria_status():
    try:
        result = subprocess.run(["myria-node", "--status"], capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except Exception as e:
        return f"Error running 'myria-node --status': {e}"

def check_status_and_alert(bot_token, chat_id):
    output = run_myria_status()
    # Required lines
    required1 = ">>>[INFO] Current Cycle Status: running"
    required2 = ">>>[INFO] Myria Node Service is running!"
    if required1 in output and required2 in output:
        # Node is online, no alert
        print(f"[{datetime.now()}] Node online, no alert sent.")
        return
    # Else send alert
    message = f"NODE IS OFFLINE!\nOutput:\n{output}"
    print(f"[{datetime.now()}] Node offline detected, sending alert.")
    send_telegram_message(bot_token, chat_id, message)

def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            bot_token = data.get("bot_token")
            chat_id = data.get("chat_id")
            if bot_token and chat_id:
