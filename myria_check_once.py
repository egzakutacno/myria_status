import subprocess
import json
import requests
import os

CONFIG_FILE = os.path.expanduser('~/.myria_monitor_config.json')

# Load config
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config['bot_token']
TELEGRAM_CHAT_ID = config['chat_id']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(message):
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        return response.ok
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False

def check_node_status():
    try:
        result = subprocess.run(['myria-node', '--status'], capture_output=True, text=True, timeout=10)
        output = result.stdout
        print(f"Status output:\n{output}")

        if "Current Cycle Status: running" in output and "Myria Node Service is running!" in output:
            send_telegram_message(f"✅ Myria Monitor started successfully!\n\nNode is healthy.\n\nStatus:\n{output}")
        else:
            send_telegram_message(f"⚠️ Myria Monitor started, but node is NOT healthy.\n\nStatus:\n{output}")
    except subprocess.TimeoutExpired:
        send_telegram_message("⏱️ Myria Node status check timed out during install.")
    except Exception as e:
        send_telegram_message(f"❌ Error during initial Myria Node status check:\n{e}")

if __name__ == "__main__":
    check_node_status()
