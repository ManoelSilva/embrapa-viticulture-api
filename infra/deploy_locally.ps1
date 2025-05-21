# Check if IP address is provided
if ($args.Count -eq 0) {
    Write-Host "Usage: .\deploy_locally.ps1 <EC2_PUBLIC_IP> <MOTHERDUCK_TOKEN"
    exit 1
}

if ($args.Count -eq 1) {
    Write-Host "Usage: .\deploy_locally.ps1 <EC2_PUBLIC_IP> <MOTHERDUCK_TOKEN>"
    exit 1
}


$MOTHERDUCK_TOKEN=$args[1]
$EC2_IP = $args[0]
$SSH_KEY_PATH = Join-Path (Join-Path $env:USERPROFILE ".ssh") "id_rsa"
$GITHUB_REPOSITORY = "manoelsilva/embrapa-viticulture-api"

$REMOTE_COMMAND = @'
set -e
USER_HOME="/home/ubuntu"
APP_DIR="$USER_HOME/embrapa-viticulture-api"
REPO_URL="https://github.com/__REPO__.git"

sudo apt-get update
sudo apt-get install -y dos2unix
sudo apt-get install -y python3-pip python3-venv git

if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git fetch --all
  git pull
  cd "$APP_DIR"
else
  rm -rf "$APP_DIR"
  git clone "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
fi

# Create .env file with MOTHERDUCK_TOKEN
cat << EOF > "$APP_DIR/.env"
MOTHERDUCK_TOKEN=__MOTHERDUCK_TOKEN__
EOF

python3 -m venv "$APP_DIR/src/venv"
source "$APP_DIR/src/venv/bin/activate"
pip install -r requirements.txt
pip install waitress

cat << EOF | sudo tee /etc/systemd/system/embrapa-viticulture.service
[Unit]
Description=Embrapa Viticulture API
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/embrapa-viticulture-api/src
Environment="PATH=/home/ubuntu/embrapa-viticulture-api/src/venv/bin"
Environment="PYTHONPATH=/home/ubuntu/embrapa-viticulture-api"
ExecStart=/home/ubuntu/embrapa-viticulture-api/src/venv/bin/waitress-serve --host=0.0.0.0 --port=5000 app:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=embrapa-viticulture

[Install]
WantedBy=multi-user.target
EOF

sudo chmod 644 /etc/systemd/system/embrapa-viticulture.service

sudo systemctl daemon-reload
sudo systemctl enable embrapa-viticulture
sudo systemctl restart embrapa-viticulture
sudo systemctl status embrapa-viticulture
'@

$REMOTE_COMMAND = $REMOTE_COMMAND -replace '__REPO__', $GITHUB_REPOSITORY
$REMOTE_COMMAND = $REMOTE_COMMAND -replace '__MOTHERDUCK_TOKEN__', $MOTHERDUCK_TOKEN

Write-Host "REMOTE_COMMAND content:"
Write-Host $REMOTE_COMMAND

Write-Host "Deploying application via SSH..."
$tmpScript = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllLines($tmpScript, $REMOTE_COMMAND -split "`n", [System.Text.Encoding]::UTF8)

Get-Content $tmpScript | ssh -i "$SSH_KEY_PATH" ubuntu@$EC2_IP 'dos2unix | bash -s'

Remove-Item $tmpScript

Write-Host "Deployment completed!"