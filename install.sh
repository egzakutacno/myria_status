#!/bin/bash
set -e

echo "Starting Myria Monitor install..."

# Check python3 and pip
if ! command -v python3 &> /dev/null; then
    echo "Installing python3..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

pip3 install --user requests
python3 -c "import zoneinfo" 2>/dev/null || pip3 install --user backports.zoneinfo

# Download monitor script
curl -fsSL https://github.com/egzakutacno/myria_status/raw/main/myria_monitor.py -o ~/myria_monitor.py
chmod +x ~/myria_monitor.py

# Ask user for Telegram credentials here (once)
read -p "Enter your Telegram Bot Token: " BOT_TOKEN
read -p "Enter your Telegram Chat ID: " CHAT_ID

# Save credentials to config file BEFORE starting service
CONFIG_FILE="$HOME/.myria_monitor_config.json"
echo "{\"bot_token\":\"$BOT_TOKEN\", \"chat_id\":\"$CHAT_ID\"}" > "$CONFIG_FILE"

# Setup systemd user service
SERVICE_FILE="$HOME/.config/systemd/user/myria-monitor.service"
mkdir -p "$(dirname "$SERVICE_FILE")"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Myria Node Monitor Service

[Service]
ExecStart=$(which python3) $HOME/myria_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable myria-monitor
systemctl --user start myria-monitor

echo "Myria Monitor installed and started as a user systemd service."
echo "Run 'journalctl --user -u myria-monitor -f' to see logs."
