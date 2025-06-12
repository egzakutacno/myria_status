#!/bin/bash

# Check and install Python3
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3
else
    echo "Python3 is already installed."
fi

# Check and install pip3
if ! command -v pip3 &> /dev/null
then
    echo "pip3 not found. Installing..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

# Install required Python packages
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
