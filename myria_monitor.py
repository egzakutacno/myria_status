#!/usr/bin/env python3
import subprocess
import requests
import time
from datetime import datetime, timedelta
import json
import os
import sys

try:
    import zoneinfo  # Python 3.9+
except ImportError:
    from backports import zoneinfo  # For Python <3.9, install backports.zoneinfo

CONFIG_PATH = os.path.expanduser("~/.myria_monitor_config.json")
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

def load_config():
    global TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                TELEGRAM_BOT_TOKEN = data.get("bot_token", "")
                TELEGRAM_CHAT_ID = data.get("chat_id", "")
        except Exception as e:
            print(f"Failed to read config file: {e}")
    else:
        print("Config file not found! Exiting.")
        sys.exit(1)

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot token or chat id not set.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        resp = requests.post(url, data=payload, timeout=10)
        if resp.ok:
            print("Sent Telegram message.")
        else:
            print(f"Failed to send Telegram message: {resp.text}")
        return resp.ok
    except Exception as e:
        print(f"Exception sending Telegram message: {e}")
        return False

def check_node_status():
    print(f"[{datetime.now().isoformat()}] Checking Myria Node status...")
    try:
        result = subprocess.run(
            ["myria-node", "--status"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = result.stdout
        print(f"Status output:\n{output}")

        if "Current Cycle Status: running" in output and "Myria Node Service is running!" in output:
            print("Node is healthy ✅")
            return True
        else:
            msg = "⚠️ Myria Node is NOT healthy on this VM.\nStatus output:\n" + output
            print(msg)
            send_telegram_message(msg)
            return False
    except subprocess.TimeoutExpired:
        msg = "⏱️ Myria Node status check timed out on this VM."
        print(msg)
        send_telegram_message(msg)
        return False
    except Exception as e:
        msg = f"❌ Error checking Myria Node status on this VM:\n{e}"
        print(msg)
        send_telegram_message(msg)
        return False

def wait_until_next_check(target_hour, target_minute, tz):
    now = datetime.now(tz)
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target_time <= now:
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    print(f"Waiting {int(wait_seconds)} seconds until next check at {target_hour:02d}:{target_minute:02d} HK time.")
    time.sleep(wait_seconds)

def main():
    tz = zoneinfo.ZoneInfo("Asia/Hong_Kong")
    load_config()

    # Run one immediate check on start
    check_node_status()

    while True:
        wait_until_next_check(8, 20, tz)
        check_node_status()

        wait_until_next_check(15, 20, tz)
        check_node_status()

if __name__ == "__main__":
    main()
