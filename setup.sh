#!/bin/bash

# Setup script for Mudpy with web frontend

echo "🛠️ Setting Up Mudpy with Persistent Storage and Web Frontend"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git and try again."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Clone Mudpy repository
echo "📥 Cloning Mudpy repository..."
git clone https://mudpy.org/code/mudpy
if [ $? -ne 0 ]; then
    echo "Failed to clone the repository. Please check your internet connection and try again."
    exit 1
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv mudpy_venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source mudpy_venv/bin/activate

# Install Mudpy and dependencies
echo "📦 Installing Mudpy and dependencies..."
cd mudpy
pip install .
cd ..
pip install websockets flask

# Create necessary directories if they don't exist
echo "📁 Creating configuration directories..."
mkdir -p config data static

# Copy configuration files if needed
if [ ! -f "config/game_config.yaml" ]; then
    cp mudpy/config/*.yaml config/ 2>/dev/null || echo "No config files to copy, will use defaults"
fi

echo "✅ Setup completed successfully!"
echo "To start the server, run: python3 start_server.py"
echo "To access the web interface, open a browser and navigate to: http://localhost:5000"
