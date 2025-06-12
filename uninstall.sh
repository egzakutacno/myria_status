#!/bin/bash

echo "🔧 Stopping the Myria Monitor service..."
sudo systemctl stop myria-monitor
sudo systemctl disable myria-monitor
sudo rm /etc/systemd/system/myria-monitor.service

echo "🗑️ Removing application files..."
sudo rm -rf /opt/myria-monitor

echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "✅ Uninstallation complete."
