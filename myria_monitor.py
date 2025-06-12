#!/usr/bin/env python3
import subprocess
import requests
import time
import os
import json
from datetime import datetime, timedelta, time as dtime

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # for Python <3.9, install backports.zoneinfo

CONFIG_FILE = os.path.expanduser("~/.myria_monitor_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def get_telegram_credentials():
    config = load_config()
    if not config.get('bot_token'):
        config['bot_token'] = input("Enter your Telegram Bot Token: ").strip()
    if not config.get('chat_id'):
        config['chat_id'] = input("Enter your Telegram Chat ID: ").strip()
    save_config(config)
    return config['bot_token'], config['chat_id']

def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=payload, timeout=10)
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
            print(f"{datetime.now()}: Myria node is healthy.")
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

def wait_until_next_check(target_times, tz):
    while True:
        now_utc = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))
        now = now_utc.astimezone(tz)
        today = now.date()

        check_datetimes = [datetime.combine(today, t, tzinfo=tz) for t in target_times]
        future_checks = [dt for dt in check_datetimes if dt > now]

        if future_checks:
            next_check = min(future_checks)
        else:
            tomorrow = today + timedelta(days=1)
            next_check = datetime.combine(tomorrow, target_times[0], tzinfo=tz)

        next_check_utc = next_check.astimezone(ZoneInfo('UTC'))
        wait_seconds = (next_check_utc - now_utc).total_seconds()

        print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Waiting {int(wait_seconds)} seconds until next check at {next_check.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        time.sleep(wait_seconds)
        yield

def main():
    bot_token, chat_id = get_telegram_credentials()
    hong_kong_tz = ZoneInfo("Asia/Hong_Kong")
    check_times = [dtime(8, 20), dtime(15, 20)]
    for _ in wait_until_next_check(check_times, hong_kong_tz):
        check_node_status(bot_token, chat_id)

if __name__ == "__main__":
    main()
