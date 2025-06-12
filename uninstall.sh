#!/bin/bash
set -e

INSTALL_DIR="$HOME/myria_monitor"

echo "Stopping Myria Monitor..."

# Kill all processes running myria_monitor.py, ignoring errors if none found
pkill -f myria_monitor.py || true

echo "Removing installation directory: $INSTALL_DIR"

# Force remove the directory and all contents (including hidden files)
rm -rf "$INSTALL_DIR"

if [ ! -d "$INSTALL_DIR" ]; then
  echo "Installation directory removed successfully."
else
  echo "Failed to remove installation directory. Please check permissions."
fi

echo "Uninstallation complete."
