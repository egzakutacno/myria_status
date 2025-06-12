#!/bin/bash
set -e

INSTALL_DIR="$HOME/myria_monitor"

echo "Stopping Myria Monitor..."

pkill -f myria_monitor.py || echo "No running myria_monitor.py process found."

echo "Removing installation directory: $INSTALL_DIR"
rm -rf "$INSTALL_DIR"

echo "Uninstallation complete."
