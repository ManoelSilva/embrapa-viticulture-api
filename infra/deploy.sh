#!/bin/bash
set -e

# Update system packages and install required tools
echo "Updating system packages and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git dos2unix

USER_HOME="/home/ubuntu"
APP_DIR="$USER_HOME/embrapa-viticulture-api"

# Remove and recreate app directory
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"

# Copy application files from /tmp/deploy
cp -r /tmp/deploy/* "$APP_DIR/"

# Verify files are copied correctly
cd "$APP_DIR"
echo "Current directory: $(pwd)"
ls -la

# Set up Python virtual environment
python3 -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"

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
WorkingDirectory=$USER_HOME/embrapa-viticulture-api
Environment="PATH=$USER_HOME/embrapa-viticulture-api/venv/bin"
Environment="PYTHONPATH=$USER_HOME/embrapa-viticulture-api"
ExecStart=$USER_HOME/embrapa-viticulture-api/venv/bin/waitress-serve --host=0.0.0.0 --port=5000 app:app
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