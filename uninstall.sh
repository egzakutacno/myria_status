#!/bin/bash

# Stop and disable the service
sudo systemctl stop myria-monitor
sudo systemctl disable myria-monitor

# Remove files
sudo rm /opt/myria_monitor.py
sudo rm /etc/systemd/system/myria-monitor.service
sudo rm /opt/config.json

# Reload systemd
sudo systemctl daemon-reload

echo "✅ Myria Node Monitor has been uninstalled."
