#!/bin/bash
set -e

REPO_URL="https://github.com/egzakutacno/myria_status/blob/main/myria_monitor.py"
INSTALL_DIR="$HOME/myria_monitor"

echo "Installing Myria Monitor..."

if [ -d "$INSTALL_DIR" ]; then
  echo "Existing installation found at $INSTALL_DIR, pulling latest changes..."
  cd "$INSTALL_DIR"
  git pull
else
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# Optional: create and activate virtualenv if you want
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

chmod +x myria_monitor.py

echo "Starting myria_monitor.py in background..."
nohup ./myria_monitor.py > myria_monitor.log 2>&1 &

echo "Installation complete. The monitor is running in background."
echo "To check logs: tail -f $INSTALL_DIR/myria_monitor.log"
