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
    const showMapButton = document.getElementById('show-map');
    const mapContainer = document.getElementById('map-container');
    const showInventoryButton = document.getElementById('show-inventory');
    const inventoryPanel = document.getElementById('inventory-panel');
    const inventoryList = document.getElementById('inventory-list');
    const equipmentList = document.getElementById('equipment-list');
    const itemDetails = document.getElementById('item-details');
    const inventoryActions = document.getElementById('inventory-actions');
    const useItemButton = document.getElementById('use-item');
    const dropItemButton = document.getElementById('drop-item');
    const toggleDarkModeButton = document.getElementById('toggle-dark-mode');
    const serverUrlInput = document.getElementById('server-url');
    const saveSettingsButton = document.getElementById('save-settings');

    // Initialize Feather icons
    feather.replace();

    // Variables
    let webSocket = null;
    let commandHistory = [];
    let historyIndex = -1;
    let roomPositions = {};
    let doorStates = {};
    let hazardStates = {};
    let powerStates = {};
    let inventoryData = null;
    let selectedItemId = null;
    let selectedRoomId = null;
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
                    } else if (data.type === 'map') {
                        roomPositions = {};
                        doorStates = data.doors || {};
                        hazardStates = data.hazards || {};
                        powerStates = data.power || {};
                        data.rooms.forEach(r => {
                            roomPositions[r.id] = { x: r.x, y: r.y, name: r.name };
                        });
                        renderMap();
                    } else if (data.type === 'inventory') {
                        inventoryData = data.inventory;
                        renderInventory();
                    } else if (data.type === 'object_data') {
                        displayObjectData(data.object);
                    } else if (data.type === 'door_status') {
                        doorStates[data.door_id] = data.locked;
                        renderMap();
                    } else if (data.type === 'atmos_warning') {
                        hazardStates[data.room_id] = data.hazards || [];
                        renderMap();
                    } else if (data.type === 'power_status') {
                        powerStates[data.grid_id] = data.is_powered;
                        renderMap();
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

    // Render map in the map container
    function renderMap() {
        if (!mapContainer) return;

        if (Object.keys(roomPositions).length === 0) {
            mapContainer.style.display = 'none';
            return;
        }

        mapContainer.style.display = 'block';

        // Determine grid bounds
        let xs = Object.values(roomPositions).map(p => p.x);
        let ys = Object.values(roomPositions).map(p => p.y);
        let minX = Math.min(...xs), maxX = Math.max(...xs);
        let minY = Math.min(...ys), maxY = Math.max(...ys);

        const rows = maxY - minY + 1;
        const cols = maxX - minX + 1;

        mapContainer.innerHTML = '';
        const grid = document.createElement('div');
        grid.className = 'map-grid';
        grid.style.gridTemplateColumns = `repeat(${cols}, 40px)`;

        for (let y = minY; y <= maxY; y++) {
            for (let x = minX; x <= maxX; x++) {
                const cell = document.createElement('div');
                cell.className = 'map-cell';
                const key = Object.keys(roomPositions).find(k => roomPositions[k].x === x && roomPositions[k].y === y);
                if (key === selectedRoomId) {
                    cell.classList.add('selected');
                }
                if (key) {
                    cell.textContent = roomPositions[key].name[0];
                    cell.title = roomPositions[key].name;
                    const overlay = document.createElement('div');
                    overlay.className = 'overlay';
                    let icons = '';
                    if (doorStates[key]) icons += '<i data-feather="lock"></i>';
                    if (hazardStates[key] && hazardStates[key].length > 0) icons += '<i data-feather="alert-triangle"></i>';
                    if (powerStates[key] === false) icons += '<i data-feather="zap-off"></i>';
                    overlay.innerHTML = icons;
                    cell.appendChild(overlay);
                    cell.addEventListener('click', () => handleMapClick(key));
                }
                grid.appendChild(cell);
            }
        }
        mapContainer.appendChild(grid);
        feather.replace();
    }

    function handleMapClick(roomId) {
        selectedRoomId = roomId;
        let msg = roomPositions[roomId].name;
        if (hazardStates[roomId] && hazardStates[roomId].length > 0) {
            msg += ' - Hazards: ' + hazardStates[roomId].join(', ');
        }
        if (doorStates[roomId]) {
            msg += ' [Door Locked]';
        }
        if (powerStates[roomId] === false) {
            msg += ' [No Power]';
        }
        appendToTerminal(msg, 'system-message');
        renderMap();
    }

    function requestMap() {
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(JSON.stringify({ type: 'map_request' }));
        }
    }

    function requestInventory() {
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(JSON.stringify({ type: 'inventory_request' }));
        }
    }

    function renderInventory() {
        if (!inventoryPanel) return;
        inventoryList.innerHTML = '';
        equipmentList.innerHTML = '';
        if (itemDetails) itemDetails.style.display = 'none';
        if (inventoryActions) inventoryActions.style.display = 'none';

        if (!inventoryData) return;

        if (inventoryData.items.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'Empty';
            inventoryList.appendChild(li);
        } else {
            inventoryData.items.forEach(it => {
                const li = document.createElement('li');
                li.textContent = it.name;
                li.dataset.objectId = it.id;
                li.className = 'inventory-item';
                if (selectedItemId === it.id) li.classList.add('selected');
                li.addEventListener('click', () => selectInventoryItem(it.id));
                inventoryList.appendChild(li);
            });
        }

        inventoryData.equipment.forEach(eq => {
            const li = document.createElement('li');
            li.textContent = `[${eq.slot}] ${eq.name}`;
            li.dataset.objectId = eq.id;
            li.className = 'inventory-item';
            if (selectedItemId === eq.id) li.classList.add('selected');
            li.addEventListener('click', () => selectInventoryItem(eq.id));
            equipmentList.appendChild(li);
        });
    }

    function requestObject(objectId) {
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(JSON.stringify({ type: 'object_request', object_id: objectId }));
        }
    }

    function findNameById(id) {
        for (const it of inventoryData.items) {
            if (it.id === id) return it.name;
        }
        for (const eq of inventoryData.equipment) {
            if (eq.id === id) return eq.name;
        }
        return null;
    }

    function selectInventoryItem(id) {
        selectedItemId = id;
        renderInventory();
        const item = inventoryData.items.find(it => it.id === id) || inventoryData.equipment.find(eq => eq.id === id);
        if (itemDetails) {
            itemDetails.textContent = item ? item.description : '';
            itemDetails.style.display = item ? 'block' : 'none';
        }
        if (inventoryActions) {
            inventoryActions.style.display = item ? 'flex' : 'none';
        }
    }

    function displayObjectData(obj) {
        if (!obj) {
            appendToTerminal('Object not found.', 'error-message');
            return;
        }
        appendToTerminal(`${obj.name}: ${obj.description}`, 'system-message');
        if (itemDetails && obj.id === selectedItemId) {
            itemDetails.textContent = obj.description;
            itemDetails.style.display = 'block';
            if (inventoryActions) inventoryActions.style.display = 'flex';
        }
        if (obj.components) {
            Object.entries(obj.components).forEach(([name, comp]) => {
                appendToTerminal(`- ${name}: ${JSON.stringify(comp)}`, 'system-message');
            });
        }
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

    showMapButton.addEventListener('click', function() {
        requestMap();
    });

    showInventoryButton.addEventListener('click', function() {
        if (inventoryPanel.style.display === 'none') {
            requestInventory();
            inventoryPanel.style.display = 'block';
        } else {
            inventoryPanel.style.display = 'none';
        }
    });

    if (useItemButton) {
        useItemButton.addEventListener('click', function() {
            if (!selectedItemId) return;
            const name = findNameById(selectedItemId);
            if (name && webSocket && webSocket.readyState === WebSocket.OPEN) {
                webSocket.send(JSON.stringify({ command: `use ${name}` }));
            }
        });
    }

    if (dropItemButton) {
        dropItemButton.addEventListener('click', function() {
            if (!selectedItemId) return;
            const name = findNameById(selectedItemId);
            if (name && webSocket && webSocket.readyState === WebSocket.OPEN) {
                webSocket.send(JSON.stringify({ command: `drop ${name}` }));
            }
        });
    }

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
