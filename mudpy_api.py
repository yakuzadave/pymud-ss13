#!/usr/bin/env python3
import os
import socket
import time
import threading
import logging
import yaml
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('mudpy_api')

class MudpyClient:
    """Interface with the MUDpy server via socket connection (similar to telnet)."""
    
    def __init__(self, host='localhost', port=4000, timeout=5):
        """Initialize a connection to the MUDpy server.
        
        Args:
            host (str): MUDpy server hostname
            port (int): MUDpy server port
            timeout (int): Socket timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.connected = False
        self.buffer = ""
        self._connect()
        
        # Set up a thread to receive data
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
        # Used for state management
        self.logged_in = False
        self.username = None
        
        # Used for data persistence
        self.data_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def _connect(self):
        """Establish a socket connection to the MUDpy server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to MUDpy server at {self.host}:{self.port}")
            
            # Read initial welcome message
            time.sleep(0.5)  # Give server time to send welcome message
        except (socket.error, socket.timeout) as e:
            logger.error(f"Failed to connect to MUDpy server: {e}")
            self.connected = False

    def _receive_loop(self):
        """Continuously receive data from the socket."""
        while self.running and self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8', errors='replace')
                if not data:
                    logger.warning("Connection closed by server")
                    self.connected = False
                    break
                    
                self.buffer += data
            except socket.timeout:
                # This is normal, just continue
                pass
            except socket.error as e:
                logger.error(f"Socket error: {e}")
                self.connected = False
                break
            
            # Prevent CPU hogging
            time.sleep(0.1)

    def get_welcome_message(self):
        """Get the welcome message from the server."""
        # Wait a bit to ensure we've received the welcome message
        time.sleep(1)
        welcome = self.buffer
        self.buffer = ""
        return welcome

    def process_command(self, command):
        """Send a command to the MUDpy server and get the response.
        
        Args:
            command (str): The command to send
            
        Returns:
            str: The server's response
        """
        if not self.connected:
            self._connect()
            if not self.connected:
                return "⚠️ Not connected to MUDpy server. Please try again later."
        
        # Clear the buffer before sending command
        self.buffer = ""
        
        try:
            # Send the command
            self.socket.sendall(f"{command}\n".encode('utf-8'))
            
            # Check for login-related commands for state management
            if "create" in command.lower() and "character" in command.lower():
                # Extract username for new character
                username_match = re.search(r'create\s+character\s+(\w+)', command.lower())
                if username_match:
                    potential_username = username_match.group(1)
                    # The login status will be confirmed by checking responses later
            
            elif "connect" in command.lower():
                # Extract username for existing character
                username_match = re.search(r'connect\s+(\w+)', command.lower())
                if username_match:
                    potential_username = username_match.group(1)
                    # The login status will be confirmed by checking responses later
            
            # Wait for a response
            time.sleep(0.5)
            
            # Get and clear the buffer
            response = self.buffer
            self.buffer = ""
            
            # Check for login confirmation in the response
            if "Welcome" in response and "You are now logged in" in response:
                self.logged_in = True
                # Try to extract username from response if we didn't get it from command
                if not hasattr(self, 'potential_username'):
                    username_match = re.search(r'Welcome,\s+(\w+)!', response)
                    if username_match:
                        self.username = username_match.group(1)
                else:
                    self.username = potential_username
                
                # Save player data
                self._save_player_data()
            
            return response
            
        except socket.error as e:
            logger.error(f"Error sending command: {e}")
            self.connected = False
            return f"⚠️ Error communicating with MUDpy server: {e}"

    def _save_player_data(self):
        """Save player data to YAML file for persistence."""
        if not self.logged_in or not self.username:
            return
            
        player_file = os.path.join(self.data_dir, 'players.yaml')
        
        # Load existing data or create new
        try:
            with open(player_file, 'r') as f:
                players_data = yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError):
            players_data = {}
        
        # Create or update player entry
        if 'players' not in players_data:
            players_data['players'] = {}
            
        # Basic player data storage
        if self.username not in players_data['players']:
            players_data['players'][self.username] = {
                'last_login': time.time(),
                'login_count': 1
            }
        else:
            players_data['players'][self.username]['last_login'] = time.time()
            players_data['players'][self.username]['login_count'] += 1
        
        # Save updated data
        try:
            with open(player_file, 'w') as f:
                yaml.dump(players_data, f)
        except Exception as e:
            logger.error(f"Error saving player data: {e}")

    def close(self):
        """Close the connection to the MUDpy server."""
        self.running = False
        if self.connected and self.socket:
            try:
                self.socket.close()
                logger.info("Connection to MUDpy server closed")
            except socket.error as e:
                logger.error(f"Error closing socket: {e}")
        self.connected = False
