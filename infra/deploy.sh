#!/bin/bash
set -e

# Variables
USER_HOME="/home/ubuntu"
APP_DIR="$USER_HOME/embrapa-viticulture-api"
REPO_URL="https://github.com/${GITHUB_REPOSITORY}.git"
COMMIT_SHA="${GITHUB_SHA}"

# Update system packages and install required tools
echo "Updating system packages and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git dos2unix

# Clone or pull latest code
echo "Deploying from $REPO_URL at commit $COMMIT_SHA"
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git fetch --all
  git reset --hard "$COMMIT_SHA"
else
  rm -rf "$APP_DIR"
  git clone "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
  git checkout "$COMMIT_SHA"
fi

# Set up Python virtual environment
python3 -m venv "$APP_DIR/src/venv"
source "$APP_DIR/src/venv/bin/activate"

# Install dependencies
pip install -r requirements.txt
pip install waitress

# Create systemd service file
cat << EOF | sudo tee /etc/systemd/system/embrapa-viticulture.service
[Unit]
Description=Embrapa Viticulture API
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=$USER_HOME/embrapa-viticulture-api/src
Environment="PATH=$USER_HOME/embrapa-viticulture-api/src/venv/bin"
Environment="PYTHONPATH=$USER_HOME/embrapa-viticulture-api"
ExecStart=$USER_HOME/embrapa-viticulture-api/src/venv/bin/waitress-serve --host=0.0.0.0 --port=5000 app:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=embrapa-viticulture

[Install]
WantedBy=multi-user.target
EOF

sudo chmod 644 /etc/systemd/system/embrapa-viticulture.service

# Reload systemd and restart the service
sudo systemctl daemon-reload
sudo systemctl enable embrapa-viticulture
sudo systemctl restart embrapa-viticulture

# Show service status and recent logs
echo "Service status:"
sudo systemctl status embrapa-viticulture

echo "Recent logs:"
sudo journalctl -u embrapa-viticulture -n 50 