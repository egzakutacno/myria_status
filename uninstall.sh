#!/bin/bash
set -e

INSTALL_DIR="$HOME/myria_monitor"

echo "Stopping Myria Monitor..."

pkill -f myria_monitor.py || true

echo "Removing installation directory: $INSTALL_DIR"

rm -rf "$INSTALL_DIR"

if [ ! -d "$INSTALL_DIR" ]; then
  echo "Installation directory removed successfully."
else
  echo "Failed to remove installation directory. Please check permissions or if files are locked."
  exit 1
fi

echo "Uninstallation complete."
