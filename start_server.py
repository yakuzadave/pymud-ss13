#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
from flask import Flask, send_from_directory

# Ensure the virtual environment is activated
venv_path = os.path.join(os.getcwd(), 'mudpy_venv')
if not os.path.exists(venv_path):
    print("Virtual environment not found. Please run setup.sh first.")
    sys.exit(1)

# Check if mudpy is installed
try:
    import websockets
except ImportError:
    print("Required packages not found. Please run setup.sh first.")
    sys.exit(1)

from websocket_server import start_websocket_server

# Start Flask app for serving static files
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

def start_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

def start_mudpy():
    # Use subprocess to start mudpy in a separate process
    try:
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            mudpy_process = subprocess.Popen(['mudpy'], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
        else:
            # If not in a virtual environment, use the one we created
            activate_script = os.path.join(venv_path, 'bin', 'activate')
            mudpy_process = subprocess.Popen(f'source {activate_script} && mudpy', 
                                           shell=True, 
                                           executable='/bin/bash',
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
        
        print("MUDpy server started!")
        return mudpy_process
    except Exception as e:
        print(f"Failed to start MUDpy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("📚 Starting MUDpy Game Server with Web Frontend")
    
    # Start MUDpy server
    print("🔄 Starting MUDpy server...")
    mudpy_process = start_mudpy()
    
    # Give MUDpy time to start up
    time.sleep(3)
    
    # Start WebSocket server in a separate thread
    print("🌐 Starting WebSocket server...")
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.daemon = True
    websocket_thread.start()
    
    # Start Flask server for web interface
    print("🖥️ Starting web interface...")
    print("✅ Server started! Access the web interface at: http://localhost:5000")
    start_flask()
