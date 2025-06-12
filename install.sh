#!/bin/bash

# Simple installer for Myria Node Monitor

echo "Installing Python and requests if not already installed..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install requests

echo "Copying the monitoring script to /opt/myria-monitor..."
sudo mkdir -p /opt/myria-monitor
sudo cp myria_monitor.py /opt/myria-monitor/

echo "Creating systemd service..."
cat <<EOT | sudo tee /etc/systemd/system/myria-monitor.service
[Unit]
Description=Myria Node Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/myria-monitor/myria_monitor.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOT

echo "Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable myria-monitor.service
sudo systemctl start myria-monitor.service

echo "✅ Installation complete! The Myria Monitor is now running in the background."
echo "You can check its status with: sudo systemctl status myria-monitor"
