# Testing Guide for PyMUD-SS13

This guide covers all aspects of testing the PyMUD-SS13 application, with special focus on the TUI client.

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Unit Testing](#unit-testing)
3. [Integration Testing](#integration-testing)
4. [BDD Testing with Behave](#bdd-testing-with-behave)
5. [End-to-End Testing](#end-to-end-testing)
6. [Testing the TUI](#testing-the-tui)
7. [Continuous Integration](#continuous-integration)
8. [Best Practices](#best-practices)

---

## Testing Overview

PyMUD-SS13 uses multiple testing strategies to ensure quality:

- **Unit Tests**: Test individual components in isolation using pytest
- **Integration Tests**: Test interactions between components
- **BDD Tests**: Behavior-driven testing using Behave for user scenarios
- **E2E Tests**: End-to-end testing with Playwright (optional)

### Test Structure

```
pymud-ss13/
├── tests/                    # Unit and integration tests
│   ├── test_*.py            # Test files
│   ├── conftest.py          # Pytest fixtures
│   └── test_tui_*.py        # TUI-specific tests
├── features/                 # BDD feature files
│   ├── *.feature            # Gherkin scenarios
│   ├── steps/               # Step definitions
│   └── environment.py       # Behave configuration
└── logs/                     # Test logs (gitignored)
    ├── tui/                 # TUI logs
    └── behave/              # Behave test logs
```

---

## Unit Testing

### Running Unit Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_tui_client.py
```

Run with coverage:
```bash
pytest --cov=tui_client --cov-report=html
```

Run with verbose output:
```bash
pytest -v
```

Run specific test class or method:
```bash
pytest tests/test_tui_client.py::TestGameClient::test_client_initialization
```

### Writing Unit Tests

Example unit test structure:

```python
import pytest
from unittest.mock import Mock, AsyncMock

from tui_client.client import GameClient


class TestGameClient:
    """Test cases for GameClient."""
    
    @pytest.fixture
    def game_client(self):
        """Create a GameClient instance."""
        app = Mock()
        return GameClient("ws://localhost:5000/ws", app)
    
    def test_initialization(self, game_client):
        """Test that client initializes correctly."""
        assert game_client.connected is False
        assert game_client.websocket is None
    
    @pytest.mark.asyncio
    async def test_connect(self, game_client, monkeypatch):
        """Test connecting to server."""
        # Mock websocket connection
        mock_ws = AsyncMock()
        monkeypatch.setattr(
            "tui_client.client.websockets.connect",
            AsyncMock(return_value=mock_ws)
        )
        
        result = await game_client.connect()
        
        assert result is True
        assert game_client.connected is True
```

### Test Fixtures

Common fixtures are defined in `tests/conftest.py`:

- `mock_app`: Mock PyMUDApp instance
- `game_client`: GameClient with mocked app
- `mock_websocket`: Mock WebSocket connection

---

## Integration Testing

Integration tests verify interactions between components:

```python
@pytest.mark.asyncio
async def test_client_server_communication():
    """Test client can communicate with server."""
    # Start test server
    server = await start_test_server()
    
    # Create client
    client = GameClient("ws://localhost:5000/ws", Mock())
    
    # Connect and send command
    await client.connect()
    await client.send_command("look")
    
    # Verify response
    # ...
    
    # Cleanup
    await client.disconnect()
    await server.stop()
```

---

## BDD Testing with Behave

### What is BDD?

Behavior-Driven Development (BDD) uses natural language to describe test scenarios.

### Running Behave Tests

Run all features:
```bash
behave
```

Run specific feature:
```bash
behave features/tui_login.feature
```

Run with specific tags:
```bash
behave --tags=@smoke
```

Run with verbose output:
```bash
behave -v
```

### Writing Feature Files

Feature files use Gherkin syntax:

```gherkin
Feature: TUI Login Flow
  As a player
  I want to log into the game through the TUI
  So that I can start playing

  Scenario: Successful login
    Given the game server is running
    And the TUI client is launched
    When I enter username "testuser"
    And I enter password "testpass123"
    And I submit the login form
    Then I should see the game screen
    And I should see a welcome message
```

### Writing Step Definitions

Step definitions map Gherkin steps to Python code:

```python
from behave import given, when, then

@given('the game server is running')
def step_server_running(context):
    """Setup a test server."""
    context.server = start_test_server()

@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in form."""
    context.entered_username = username

@then('I should see the game screen')
def step_see_game_screen(context):
    """Verify game screen is visible."""
    assert context.current_screen == "game"
```

### Available Feature Files

- `tui_login.feature`: Login and authentication flows
- `tui_game_commands.feature`: Command execution and history
- `tui_view_switching.feature`: Switching between views (F1-F5)
- `tui_inventory.feature`: Inventory management
- `tui_map_navigation.feature`: **NEW** - Map viewing, navigation, and overlays
- `tui_chat_system.feature`: **NEW** - Chat channels, messaging, and notifications
- `tui_help_system.feature`: **NEW** - Help documentation and tutorials

### New BDD Scenarios (BATCH-003)

#### Map Navigation (`tui_map_navigation.feature`)

Tests comprehensive map interaction features:
- **View station map** - Display grid layout with player position
- **Navigate with arrow keys** - Scroll viewport in all directions
- **View room details** - Click rooms to see details sidebar
- **Toggle overlays** - Door locks (D), atmosphere (A), power (P)
- **Zoom controls** - Zoom in (+) and out (-) functionality
- **Center on player** - Quick center (C) to player position
- **Minimap indicator** - Corner minimap with nearby rooms
- **Real-time updates** - Map updates as game state changes
- **Preserve state** - Map state maintained when switching views

**Example Scenario:**
```gherkin
Scenario: Navigate map with arrow keys
  Given I am viewing the map screen
  When I press the right arrow key
  Then the map viewport should scroll right
  When I press the down arrow key
  Then the map viewport should scroll down
```

#### Chat System (`tui_chat_system.feature`)

Tests all chat and communication features:
- **Send messages** - Global, local, and department channels
- **Chat history** - Scroll through message history
- **Channel switching** - Press 1-3 to switch channels (Global/Local/Dept)
- **Private messages** - Send PMs with `pm username message`
- **Notifications** - Badge indicators for new messages
- **Message filtering** - Filter by message type
- **Player muting** - Right-click to mute players
- **Online players list** - View players with status and roles
- **Emotes** - Use emote command for actions
- **Autocomplete** - Tab completion for commands
- **Timestamps** - Messages show time in HH:MM format

**Example Scenario:**
```gherkin
Scenario: Switch between chat channels
  Given I am viewing the chat screen
  When I press "1" to switch to global channel
  Then the channel indicator should show "Global"
  And I should see global chat messages
  When I press "2" to switch to local channel
  Then the channel indicator should show "Local"
  And I should see only local chat messages
```

#### Help System (`tui_help_system.feature`)

Tests help documentation and learning features:
- **Open help screen** - F4 to access help
- **Browse categories** - Navigate help by category
- **View command details** - Detailed syntax and examples
- **Search topics** - Search box with ranked results
- **Keyboard shortcuts** - Reference for all shortcuts
- **Job-specific guides** - Instructions for each role
- **Game mechanics** - Atmosphere, power, combat explanations
- **Copy examples** - Copy command examples to clipboard
- **Navigation history** - Back/forward through help pages
- **Getting started** - Step-by-step tutorial for new players
- **Context-sensitive** - Opens to relevant topic based on context
- **Recent updates** - Patch notes and what's new
- **Export content** - Save help as text file
- **Quick navigation** - Press letter to jump to topics

**Example Scenario:**
```gherkin
Scenario: Search for help topics
  Given I am viewing the help screen
  When I type "inventory" in the search box
  Then I should see search results for "inventory"
  And results should be ranked by relevance
  And I should see matching commands and articles
  When I click on a search result
  Then I should navigate to that help topic
```

### Running New BDD Tests

Run all new scenarios:
```bash
behave features/tui_map_navigation.feature
behave features/tui_chat_system.feature
behave features/tui_help_system.feature
```

Run specific scenarios by line number:
```bash
behave features/tui_map_navigation.feature:12
behave features/tui_chat_system.feature:25
```

Run all TUI features:
```bash
behave features/tui_*.feature
```

### Step Definitions Coverage

All new scenarios have complete step definitions in `features/steps/tui_steps.py`:
- **65+ new step definitions** added for map, chat, and help features
- Steps use mocking for isolation (no real server needed)
- Steps follow existing patterns and conventions
- Each step has a docstring explaining its purpose

---

## End-to-End Testing

E2E tests verify the complete user experience.

### Playwright Setup (Optional)

Install Playwright:
```bash
pip install playwright
playwright install
```

### Running E2E Tests

```bash
pytest -m e2e tests/test_tui_playwright.py
```

Note: E2E tests are marked with `@pytest.mark.skip` by default as they require special setup.

---

## Testing the TUI

### Manual TUI Testing

1. Start the server:
   ```bash
   python run_server.py
   ```

2. Launch the TUI client:
   ```bash
   python -m tui_client
   ```

3. Test checklist:
   - [ ] Login screen displays correctly
   - [ ] Can create new account
   - [ ] Can login with existing account
   - [ ] F1-F5 keys switch views
   - [ ] Commands execute and show output
   - [ ] Up/Down arrows navigate history
   - [ ] Messages display in correct colors
   - [ ] Status bar updates correctly
   - [ ] Can view inventory
   - [ ] Can view map
   - [ ] Help screen shows documentation

### TUI-Specific Tests

Run TUI-specific unit tests:
```bash
pytest tests/test_tui_client.py tests/test_tui_logging.py -v
```

### Testing Logging

Check log files after running TUI:
```bash
# View latest TUI log
ls -lt logs/tui/ | head -5

# View log content
tail -50 logs/tui/tui_YYYYMMDD_HHMMSS.log

# View debug log
tail -50 logs/tui/tui_debug_YYYYMMDD_HHMMSS.log
```

Test logging programmatically:
```python
from tui_client.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Test message")
logger.error("Error message")
logger.debug("Debug message")
```

---

## Continuous Integration

### GitHub Actions

Tests run automatically on push and pull requests.

See `.github/workflows/test.yml` for configuration.

### Coverage Reports

Coverage reports are generated in:
- `htmlcov/index.html` - View in browser
- Terminal output during test run

Minimum coverage target: 70%

---

## Best Practices

### General Testing

1. **Write tests first** (TDD approach when possible)
2. **One assertion per test** (or closely related assertions)
3. **Use descriptive test names** - `test_login_with_invalid_credentials`
4. **Mock external dependencies** - Don't test third-party code
5. **Keep tests independent** - No test should depend on another
6. **Clean up after tests** - Use fixtures and teardown
7. **Test edge cases** - Empty inputs, null values, boundary conditions

### TUI Testing

1. **Test user flows** - Not just individual functions
2. **Verify visual output** - Check colors, formatting, layout
3. **Test keyboard shortcuts** - All keybindings should work
4. **Test with real server** - At least in integration tests
5. **Check error handling** - What happens when server disconnects?
6. **Test accessibility** - Can users navigate without mouse?

### BDD Testing

1. **Use business language** - Write scenarios stakeholders can read
2. **Focus on behavior** - Not implementation details
3. **Keep scenarios focused** - One scenario = one behavior
4. **Reuse step definitions** - Don't duplicate code
5. **Use background wisely** - For common setup steps

### Performance Testing

1. **Set baselines** - Know your performance targets
2. **Test at scale** - What happens with 1000 messages?
3. **Profile bottlenecks** - Use pytest-benchmark
4. **Test memory usage** - Watch for memory leaks
5. **Test responsiveness** - UI should stay responsive

---

## Troubleshooting

### Common Issues

**Tests hang or timeout:**
- Check for deadlocks in async code
- Increase timeout values
- Verify mock objects are configured correctly

**Import errors:**
- Ensure PYTHONPATH includes project root
- Check for circular imports
- Verify all dependencies are installed

**Flaky tests:**
- Add appropriate waits for async operations
- Don't rely on timing-based assertions
- Use proper mocking to control test conditions

**Coverage not showing:**
- Run with `--cov` flag
- Check .coveragerc configuration
- Ensure test files are being discovered

### Debug Mode

Run tests with debugging:
```bash
pytest --pdb  # Drop into debugger on failure
pytest -x     # Stop on first failure
pytest -v -s  # Verbose with print statements
```

Enable TUI debug logging:
```python
from tui_client.logging_config import TUILogger
import logging

tui_logger = TUILogger()
tui_logger.set_level(logging.DEBUG)
```

---

## Contributing Tests

When adding new features:

1. Write unit tests for new functions/classes
2. Add integration tests for component interactions
3. Create BDD scenarios for user-facing features
4. Update this guide if adding new test types
5. Ensure all tests pass before submitting PR
6. Maintain or improve code coverage

---

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Behave documentation](https://behave.readthedocs.io/)
- [Playwright documentation](https://playwright.dev/python/)
- [Textual testing guide](https://textual.textualize.io/guide/testing/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Last Updated:** 2025-12-19
