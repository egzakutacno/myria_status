#!/bin/bash
set -e

REPO_URL="https://github.com/egzakutacno/myria_status.git"
INSTALL_DIR="$HOME/myria_monitor"

echo "Installing Myria Monitor..."

if [ -d "$INSTALL_DIR" ]; then
  echo "Existing installation found, pulling latest changes..."
  cd "$INSTALL_DIR"
  git pull
else
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

chmod +x myria_monitor.py

echo -n "Enter your Telegram Bot Token: "
read BOT_TOKEN
echo -n "Enter your Telegram Chat ID: "
read CHAT_ID

cat > config.json <<EOF
{
  "bot_token": "$BOT_TOKEN",
  "chat_id": "$CHAT_ID"
}
EOF

echo "Starting myria_monitor.py in background..."
nohup ./myria_monitor.py > myria_monitor.log 2>&1 &

echo "Installation complete. The monitor is running in background."
echo "To check logs: tail -f $INSTALL_DIR/myria_monitor.log"
