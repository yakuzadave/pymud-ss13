// WebSocket connection
let socket = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY = 3000; // 3 seconds

// DOM Elements
const outputElement = document.getElementById('output');
const commandInput = document.getElementById('command-input');
const sendButton = document.getElementById('send-btn');
const clearButton = document.getElementById('clear-btn');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const commandButtons = document.querySelectorAll('.cmd-btn');
const directionButtons = document.querySelectorAll('.dir-btn');

// Connect to WebSocket server
function connectWebSocket() {
    updateConnectionStatus('connecting');
    
    // Determine the WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:8000`;
    
    socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
        console.log('WebSocket connection established');
        updateConnectionStatus('connected');
        reconnectAttempts = 0;
        appendToOutput('Connected to MUDpy server!\n');
    };
    
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'message') {
                appendToOutput(data.content);
            }
        } catch (error) {
            // Fallback for non-JSON messages
            appendToOutput(event.data);
        }
    };
    
    socket.onclose = (event) => {
        console.log('WebSocket connection closed', event);
        updateConnectionStatus('disconnected');
        
        // Attempt to reconnect
        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttempts++;
            const delay = RECONNECT_DELAY * reconnectAttempts;
            appendToOutput(`\nConnection lost. Attempting to reconnect in ${delay/1000} seconds...\n`);
            
            setTimeout(() => {
                connectWebSocket();
            }, delay);
        } else {
            appendToOutput('\nFailed to reconnect after multiple attempts. Please refresh the page to try again.\n');
        }
    };
    
    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        appendToOutput('\nError with WebSocket connection.\n');
    };
}

// Update connection status indicator
function updateConnectionStatus(status) {
    statusIndicator.className = '';
    statusIndicator.classList.add(`status-${status}`);
    
    switch (status) {
        case 'connected':
            statusText.textContent = 'Connected';
            break;
        case 'disconnected':
            statusText.textContent = 'Disconnected';
            break;
        case 'connecting':
            statusText.textContent = 'Connecting...';
            break;
    }
}

// Send command to server
function sendCommand(command) {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        appendToOutput('Not connected to server. Attempting to reconnect...\n');
        connectWebSocket();
        return;
    }
    
    // Display the command in the output
    appendToOutput(`> ${command}\n`);
    
    try {
        // Send the command as JSON
        socket.send(JSON.stringify({
            command: command
        }));
    } catch (error) {
        // Fallback to plain text if JSON fails
        socket.send(command);
    }
    
    // Clear input field
    commandInput.value = '';
}

// Append text to the output element
function appendToOutput(text) {
    if (!text) return;
    
    // Process ANSI color codes if present (basic implementation)
    // This doesn't handle all ANSI codes, just a simplified version
    text = text.replace(/\x1B\[([0-9;]+)m/g, (match, p1) => {
        // Simplified ANSI code handling - could be expanded for more codes
        if (p1 === '0') return '</span>'; // Reset
        if (p1 === '31') return '<span style="color: #e74c3c;">'; // Red
        if (p1 === '32') return '<span style="color: #2ecc71;">'; // Green
        if (p1 === '33') return '<span style="color: #f1c40f;">'; // Yellow
        if (p1 === '34') return '<span style="color: #3498db;">'; // Blue
        if (p1 === '35') return '<span style="color: #9b59b6;">'; // Magenta
        if (p1 === '36') return '<span style="color: #1abc9c;">'; // Cyan
        return '';
    });
    
    // Add the text to the output
    outputElement.innerHTML += text;
    
    // Scroll to the bottom
    outputElement.scrollTop = outputElement.scrollHeight;
}

// Clear the output
function clearOutput() {
    outputElement.innerHTML = '';
}

// Event listeners
window.addEventListener('load', () => {
    connectWebSocket();
    
    commandInput.focus();
});

sendButton.addEventListener('click', () => {
    const command = commandInput.value.trim();
    if (command) {
        sendCommand(command);
    }
});

commandInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const command = commandInput.value.trim();
        if (command) {
            sendCommand(command);
        }
    }
});

clearButton.addEventListener('click', clearOutput);

// Command buttons
commandButtons.forEach(button => {
    button.addEventListener('click', () => {
        const command = button.getAttribute('data-command');
        sendCommand(command);
        commandInput.focus();
    });
});

// Direction buttons
directionButtons.forEach(button => {
    button.addEventListener('click', () => {
        const direction = button.getAttribute('data-command');
        sendCommand(direction);
        commandInput.focus();
    });
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        // Check connection when tab becomes visible again
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            appendToOutput('Reconnecting after tab became active...\n');
            connectWebSocket();
        }
    }
});
