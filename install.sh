#!/bin/bash
set -e

echo "Starting Myria Monitor install..."

# Install Python 3 if missing
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found, installing..."
  sudo apt-get update && sudo apt-get install -y python3
fi

# Install pip3 if missing
if ! command -v pip3 >/dev/null 2>&1; then
  echo "pip3 not found, installing..."
  sudo apt-get update && sudo apt-get install -y python3-pip
fi

# Install required Python packages
pip3 install --user requests
python3 -c "import zoneinfo" 2>/dev/null || pip3 install --user backports.zoneinfo

# Download the monitoring script
curl -fsSL https://github.com/egzakutacno/myria_status/raw/main/myria_monitor.py -o "$HOME/myria_monitor.py"
chmod +x "$HOME/myria_monitor.py"

# Ask user for Telegram credentials
read -p "Enter your Telegram Bot Token: " BOT_TOKEN
read -p "Enter your Telegram Chat ID: " CHAT_ID

# Save config file
CONFIG_FILE="$HOME/.myria_monitor_config.json"
echo "{\"bot_token\":\"$BOT_TOKEN\", \"chat_id\":\"$CHAT_ID\"}" > "$CONFIG_FILE"

# Setup systemd user service
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
SERVICE_FILE="$SERVICE_DIR/myria-monitor.service"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Myria Node Monitor Service

[Service]
ExecStart=$(command -v python3) $HOME/myria_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Reload systemd and enable/start service
systemctl --user daemon-reload
systemctl --user enable myria-monitor
systemctl --user start myria-monitor

echo "Myria Monitor installed and started as a user systemd service."
echo "Run 'journalctl --user -u myria-monitor -f' to see logs."
