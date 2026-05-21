#!/bin/bash

echo "🚀 ARIYANTO AI v3 - Installer"
echo "================================"

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv git redis-server tmux htop curl

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Create project directory
echo "📁 Setting up project..."
PROJECT_DIR="$HOME/ariyanto-ai-v3"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Clone or update repo
if [ -d ".git" ]; then
    echo "📥 Updating existing repo..."
    git pull
else
    echo "📥 Cloning repo..."
    git clone https://github.com/chainsighthq/ariyanto-ai-v3.git .
fi

# Setup virtual environment
echo "🐍 Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p logs data backups

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start:"
echo "  cd $PROJECT_DIR"
echo "  source .venv/bin/activate"
echo "  PYTHONPATH=src python run.py \"Long BTC 10x\""
echo ""
echo "To start production:"
echo "  sudo systemctl start ariyanto-ai"
echo ""
