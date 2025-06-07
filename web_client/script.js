document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const terminal = document.getElementById('terminal');
    const commandInput = document.getElementById('command-input');
    const sendButton = document.getElementById('send-button');
    const historyList = document.getElementById('history-list');
    const statusIndicator = document.getElementById('status-indicator');
    const connectionStatus = document.getElementById('connection-status');
    const toggleHelpButton = document.getElementById('toggle-help');
    const helpPanel = document.getElementById('help-panel');
    const clearTerminalButton = document.getElementById('clear-terminal');
    const toggleDarkModeButton = document.getElementById('toggle-dark-mode');
    const serverUrlInput = document.getElementById('server-url');
    const saveSettingsButton = document.getElementById('save-settings');

    // Initialize Feather icons
    feather.replace();

    // Variables
    let webSocket = null;
    let commandHistory = [];
    let historyIndex = -1;
    // Set dark mode to true by default
    let darkModeEnabled = localStorage.getItem('darkMode') !== 'false';

    // Determine the correct WebSocket URL based on the current location
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Use the same host (including port) as the web page
    const host = window.location.host;
    // Connect to the WebSocket endpoint at /ws
    let serverUrl = localStorage.getItem('serverUrl') || `${protocol}//${host}/ws`;

    // Set initial server URL
    serverUrlInput.value = serverUrl;

    // Apply dark mode if enabled
    if (darkModeEnabled) {
        document.body.classList.add('dark-mode');
        toggleDarkModeButton.innerHTML = '<i data-feather="sun"></i> Light Mode';
        feather.replace();
    }

    // Connect to WebSocket server
    function connectToServer() {
        if (webSocket) {
            webSocket.close();
        }

        try {
            webSocket = new WebSocket(serverUrl);

            webSocket.onopen = function() {
                updateConnectionStatus(true);
                appendToTerminal('Connected to MUDpy server.', 'system-message');
            };

            webSocket.onclose = function() {
                updateConnectionStatus(false);
                appendToTerminal('Disconnected from MUDpy server.', 'system-message');

                // Try to reconnect after 5 seconds
                setTimeout(connectToServer, 5000);
            };

            webSocket.onerror = function(error) {
                updateConnectionStatus(false);
                appendToTerminal('WebSocket error: ' + error.message, 'error-message');
            };

            webSocket.onmessage = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    console.log('Received message:', data);

                    if (data.type === 'error') {
                        appendToTerminal(data.message, 'error-message');
                    } else if (data.type === 'system') {
                        appendToTerminal(data.message, 'system-message');
                    } else if (data.type === 'response') {
                        appendToTerminal(data.message);
                    } else if (data.type === 'broadcast') {
                        appendToTerminal(data.message, 'broadcast-message');
                    } else if (data.type === 'location') {
                        appendToTerminal(data.message, 'location-message');
                    } else if (data.type === 'chat') {
                        appendToTerminal(data.message, 'chat-message');
                    } else {
                        appendToTerminal(data.message || 'Unknown message type: ' + data.type);
                    }
                } catch (e) {
                    console.error('Error parsing message:', e, event.data);
                    // If not JSON, just display the raw message
                    appendToTerminal(event.data);
                }
            };
        } catch (error) {
            appendToTerminal('Failed to connect: ' + error.message, 'error-message');
        }
    }

    // Update connection status indicator
    function updateConnectionStatus(connected) {
        if (connected) {
            statusIndicator.classList.add('connected');
            connectionStatus.textContent = 'Connected';
        } else {
            statusIndicator.classList.remove('connected');
            connectionStatus.textContent = 'Disconnected';
        }
    }

    // Append message to terminal
    function appendToTerminal(message, className = '') {
        const messageElement = document.createElement('div');
        messageElement.className = className;
        messageElement.textContent = message;

        terminal.appendChild(messageElement);

        // Scroll to bottom
        terminal.scrollTop = terminal.scrollHeight;
    }

    // Send command to server
    function sendCommand() {
        const command = commandInput.value.trim();

        if (command === '') {
            return;
        }

        // Add to history if it's not the same as the last command
        if (commandHistory.length === 0 || commandHistory[commandHistory.length - 1] !== command) {
            commandHistory.push(command);
            updateHistoryList();
        }

        // Reset history index
        historyIndex = -1;

        // Echo command to terminal
        appendToTerminal('> ' + command, 'command-echo');

        // Send to server if connected
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(JSON.stringify({ command: command }));
        } else {
            appendToTerminal('Not connected to server.', 'error-message');
            connectToServer(); // Try to reconnect
        }

        // Clear input
        commandInput.value = '';
    }

    // Update history list
    function updateHistoryList() {
        historyList.innerHTML = '';

        // Only show the last 10 commands
        const recentCommands = commandHistory.slice(-10).reverse();

        recentCommands.forEach(cmd => {
            const li = document.createElement('li');
            li.textContent = cmd;
            li.addEventListener('click', function() {
                commandInput.value = cmd;
                commandInput.focus();
            });
            historyList.appendChild(li);
        });
    }

    // Event Listeners
    sendButton.addEventListener('click', sendCommand);

    commandInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendCommand();
        } else if (event.key === 'ArrowUp') {
            // Navigate up through history
            if (commandHistory.length > 0) {
                historyIndex = (historyIndex < commandHistory.length - 1) ?
                    historyIndex + 1 : commandHistory.length - 1;
                commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            }
            event.preventDefault();
        } else if (event.key === 'ArrowDown') {
            // Navigate down through history
            if (historyIndex > 0) {
                historyIndex--;
                commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            } else if (historyIndex === 0) {
                historyIndex = -1;
                commandInput.value = '';
            }
            event.preventDefault();
        }
    });

    toggleHelpButton.addEventListener('click', function() {
        helpPanel.style.display = helpPanel.style.display === 'none' ? 'block' : 'none';
    });

    clearTerminalButton.addEventListener('click', function() {
        terminal.innerHTML = '';
        appendToTerminal('Terminal cleared.', 'system-message');
    });

    toggleDarkModeButton.addEventListener('click', function() {
        darkModeEnabled = !darkModeEnabled;
        document.body.classList.toggle('dark-mode');

        if (darkModeEnabled) {
            toggleDarkModeButton.innerHTML = '<i data-feather="sun"></i> Light Mode';
        } else {
            toggleDarkModeButton.innerHTML = '<i data-feather="moon"></i> Dark Mode';
        }

        feather.replace();
        localStorage.setItem('darkMode', darkModeEnabled);
    });

    saveSettingsButton.addEventListener('click', function() {
        const newServerUrl = serverUrlInput.value.trim();

        if (newServerUrl !== '') {
            serverUrl = newServerUrl;
            localStorage.setItem('serverUrl', serverUrl);

            // Close current modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('settings-modal'));
            modal.hide();

            // Connect to new server
            appendToTerminal('Connecting to ' + serverUrl, 'system-message');
            connectToServer();
        }
    });

    // Initial connection
    appendToTerminal('MUDpy Web Client initialized.', 'system-message');
    appendToTerminal('Connecting to ' + serverUrl + '...', 'system-message');
    connectToServer();

    // Focus on input
    commandInput.focus();
});
