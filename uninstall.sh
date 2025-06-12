#!/bin/bash
set -e

echo "Stopping and disabling Myria Monitor service..."

systemctl --user stop myria-monitor.service || true
systemctl --user disable myria-monitor.service || true

SERVICE_FILE="$HOME/.config/systemd/user/myria-monitor.service"
if [ -f "$SERVICE_FILE" ]; then
  rm "$SERVICE_FILE"
  echo "Removed systemd service file."
else
  echo "Service file not found, skipping."
fi

systemctl --user daemon-reload

if [ -f "$HOME/myria_monitor.py" ]; then
  rm "$HOME/myria_monitor.py"
  echo "Removed monitor script."
else
  echo "Monitor script not found, skipping."
fi

CONFIG_FILE="$HOME/.myria_monitor_config.json"
if [ -f "$CONFIG_FILE" ]; then
  rm "$CONFIG_FILE"
  echo "Removed config file."
else
  echo "Config file not found, skipping."
fi

echo "Uninstallation complete."
