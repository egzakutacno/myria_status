#!/bin/bash
set -e

echo "Stopping and disabling Myria Monitor service..."

# Stop and disable the user systemd service
systemctl --user stop myria-monitor.service || true
systemctl --user disable myria-monitor.service || true

# Remove the service file
SERVICE_FILE="$HOME/.config/systemd/user/myria-monitor.service"
if [ -f "$SERVICE_FILE" ]; then
    rm "$SERVICE_FILE"
    echo "Removed systemd service file."
else
    echo "Service file not found, skipping removal."
fi

# Reload systemd daemon
systemctl --user daemon-reload

# Remove the monitor script and config file
if [ -f "$HOME/myria_monitor.py" ]; then
    rm "$HOME/myria_monitor.py"
    echo "Removed monitor script."
else
    echo "Monitor script not found, skipping removal."
fi

CONFIG_FILE="$HOME/.myria_monitor_config.json"
if [ -f "$CONFIG_FILE" ]; then
    rm "$CONFIG_FILE"
    echo "Removed config file."
else
    echo "Config file not found, skipping removal."
fi

echo "Uninstallation complete."
