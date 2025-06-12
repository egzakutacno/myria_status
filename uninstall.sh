#!/bin/bash

# Stop the systemd service
sudo systemctl stop myria-monitor.service

# Disable the service
sudo systemctl disable myria-monitor.service

# Remove the service file
sudo rm -f /etc/systemd/system/myria-monitor.service

# Reload systemd to acknowledge the removal
sudo systemctl daemon-reload

# Remove the application folder (adjust path if needed)
rm -rf ~/myria_status

# Optional: remove logs or temporary files if you created them elsewhere
# Example:
# rm -f /var/log/myria-monitor.log

echo "✅ Myria Monitor uninstalled successfully."
