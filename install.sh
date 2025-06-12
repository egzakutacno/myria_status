#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install requests schedule pytz

# Download the monitor script
wget -O /opt/myria_monitor.py https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO/raw/main/myria_monitor.py
chmod +x /opt/myria_monitor.py

# Create systemd service
cat <<EOF | sudo tee /etc/systemd/system/myria-monitor.service
[Unit]
Description=Myria Node Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/myria_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable myria-monitor
sudo systemctl start myria-monitor

echo "✅ Myria Node Monitor installed and running."
