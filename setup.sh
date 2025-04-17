#!/bin/bash

# Setup script for MUDpy with WebSocket interface
# This script will:
# 1. Clone the MUDpy repository
# 2. Create a virtual environment
# 3. Install necessary packages
# 4. Set up initial configuration

echo "🛠️ Setting up MUDpy with WebSocket interface..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git and try again."
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Clone MUDpy repository
echo "📥 Cloning MUDpy repository..."
git clone https://mudpy.org/code/mudpy
if [ ! -d "mudpy" ]; then
    echo "❌ Failed to clone MUDpy repository. Please check your internet connection and try again."
    exit 1
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv mudpy_venv
if [ ! -d "mudpy_venv" ]; then
    echo "❌ Failed to create virtual environment. Please check your Python installation and try again."
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source mudpy_venv/bin/activate

# Install MUDpy
echo "📦 Installing MUDpy..."
cd mudpy && pip install . && cd ..

# Install additional required packages
echo "📦 Installing additional packages..."
pip install websockets aiohttp

# Create necessary directories if they don't exist
mkdir -p web_client

echo "✅ Setup complete! You can now run 'python start_server.py' to start the MUDpy server with WebSocket interface."
echo "🌐 The web client will be available at http://localhost:5000"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "source mudpy_venv/bin/activate"
