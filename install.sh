#!/bin/bash
set -e

echo "Starting Myria Monitor install..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found, installing..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

# Check if pip installed requests and backports.zoneinfo
pip3 install --user requests
python3 -c "import zoneinfo" 2>/dev/null || pip3 install --user backports.zoneinfo

# Download the script
curl -fsSL https://github.com/egzakutacno/myria_status/blob/main/myria_monitor.py -o ~/myria_monitor.py

chmod +x ~/myria_monitor.py

# Create systemd service
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

# Enable and start user systemd service
systemctl --user daemon-reload
systemctl --user enable myria-monitor
systemctl --user start myria-monitor

echo "Myria Monitor installed and started as a user systemd service."
echo "Run 'journalctl --user -u myria-monitor -f' to see logs."
echo "On first run, you will be prompted for your Telegram Bot Token and Chat ID."

