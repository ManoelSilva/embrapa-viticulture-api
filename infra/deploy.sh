#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv git

# Create application directory
APP_DIR="/opt/embrapa-viticulture-api"
sudo mkdir -p $APP_DIR
sudo chown ubuntu:ubuntu $APP_DIR

# Clone the repository
cd $APP_DIR
git clone https://github.com/$GITHUB_REPOSITORY.git .

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/embrapa-viticulture.service << EOF
[Unit]
Description=Embrapa Viticulture API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/waitress-serve --host=0.0.0.0 --port=5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl enable embrapa-viticulture
sudo systemctl start embrapa-viticulture

# Check service status
sudo systemctl status embrapa-viticulture 