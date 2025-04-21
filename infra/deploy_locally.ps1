# Check if IP address is provided
if ($args.Count -eq 0) {
    Write-Host "Usage: .\deploy_app.ps1 <EC2_PUBLIC_IP>"
    exit 1
}

$EC2_IP = $args[0]

# Get the current directory (where the script is located)
$SCRIPT_DIR = $PSScriptRoot
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR

# Create a temporary directory for the deployment package
$TEMP_DIR = Join-Path $env:TEMP "deploy_$(Get-Random)"
New-Item -ItemType Directory -Path $TEMP_DIR -Force
$DEPLOY_DIR = Join-Path $TEMP_DIR "deploy"
New-Item -ItemType Directory -Path $DEPLOY_DIR -Force

# Create deployment structure
New-Item -ItemType Directory -Path (Join-Path $DEPLOY_DIR "service") -Force
New-Item -ItemType Directory -Path (Join-Path $DEPLOY_DIR "routes") -Force
New-Item -ItemType Directory -Path (Join-Path $DEPLOY_DIR "config") -Force

# Copy necessary files
Copy-Item (Join-Path $PROJECT_ROOT "app.py") $DEPLOY_DIR -Force
Copy-Item (Join-Path $PROJECT_ROOT "requirements.txt") $DEPLOY_DIR -Force
Copy-Item (Join-Path $PROJECT_ROOT "logger_serialize.py") $DEPLOY_DIR -Force
Copy-Item (Join-Path $PROJECT_ROOT "service\*") (Join-Path $DEPLOY_DIR "service") -Recurse -Force
Copy-Item (Join-Path $PROJECT_ROOT "routes\*") (Join-Path $DEPLOY_DIR "routes") -Recurse -Force
Copy-Item (Join-Path $PROJECT_ROOT "config\*") (Join-Path $DEPLOY_DIR "config") -Recurse -Force

# Create deployment script with Unix line endings
$SETUP_SCRIPT = @'
#!/bin/bash

# Update system packages and install required tools
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git dos2unix

# Get the home directory for the ubuntu user
USER_HOME="/home/ubuntu"
APP_DIR="$USER_HOME/embrapa-viticulture-api"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"

# Copy application files to the application directory
echo "Copying files to $APP_DIR"
cp -r /tmp/deploy/* "$APP_DIR/"

# Verify files are copied correctly
echo "Verifying files in $APP_DIR"
cd "$APP_DIR"
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Create and activate virtual environment
echo "Setting up virtual environment"
python3 -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"

# Install dependencies including waitress
echo "Installing dependencies"
pip install -r requirements.txt
pip install waitress

# Verify waitress installation
echo "Verifying waitress installation"
which waitress-serve
ls -la "$APP_DIR/venv/bin/waitress-serve"

# Create systemd service file
echo "Creating systemd service"
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

# Set proper permissions for the service file
sudo chmod 644 /etc/systemd/system/embrapa-viticulture.service

# Reload systemd and start the service
echo "Starting service"
sudo systemctl daemon-reload
sudo systemctl enable embrapa-viticulture
sudo systemctl start embrapa-viticulture

# Check service status
echo "Service status:"
sudo systemctl status embrapa-viticulture

# Show recent logs
echo "Recent logs:"
sudo journalctl -u embrapa-viticulture -n 50
'@

# Save setup script with Unix line endings
$SETUP_SCRIPT | Out-File -FilePath (Join-Path $DEPLOY_DIR "setup.sh") -Encoding ASCII -NoNewline
Add-Content -Path (Join-Path $DEPLOY_DIR "setup.sh") -Value "`n" -NoNewline

# Create deployment package using tar
$DEPLOY_PACKAGE = Join-Path $TEMP_DIR "deploy.tar"

# Create tar file without compression to avoid permission issues
Push-Location $DEPLOY_DIR
& tar -cf $DEPLOY_PACKAGE *
Pop-Location

# Get SSH key path
$SSH_KEY_PATH = Join-Path (Join-Path $env:USERPROFILE ".ssh") "id_rsa"

# Copy deployment package to EC2
Write-Host "Copying deployment package to EC2..."
$SCP_COMMAND = "scp -i `"$SSH_KEY_PATH`" $DEPLOY_PACKAGE ubuntu@$EC2_IP`:/tmp/"
Invoke-Expression $SCP_COMMAND

# SSH into EC2 and deploy
Write-Host "Deploying application..."
$SSH_COMMAND = "ssh -i `"$SSH_KEY_PATH`" ubuntu@$EC2_IP `"cd /tmp && mkdir -p deploy && tar -xf deploy.tar -C deploy && cd deploy && dos2unix setup.sh && chmod +x setup.sh && ./setup.sh`""
Invoke-Expression $SSH_COMMAND

# Cleanup
Write-Host "Cleaning up temporary files..."
Remove-Item -Path $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Deployment completed!"