# Test Organization and Best Practices

**Project**: PyMUD-SS13  
**Created**: 2026-01-13  
**Purpose**: Document test structure, patterns, and best practices

---

## Table of Contents

1. [Test Structure Overview](#test-structure-overview)
2. [Test Categories](#test-categories)
3. [Naming Conventions](#naming-conventions)
4. [Testing Patterns](#testing-patterns)
5. [Fixtures and Mocking](#fixtures-and-mocking)
6. [Running Tests](#running-tests)
7. [Best Practices](#best-practices)

---

## Test Structure Overview

PyMUD-SS13 has a comprehensive test suite with **78 test files** covering:

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── ai_tools.py              # AI testing utilities
├── test_*.py                # Unit and integration tests (76 files)
├── README_TUI_TESTS.md      # TUI-specific test documentation
└── manual_websocket_map.py  # Manual testing utilities
```

### Test Distribution by Category

| Category | Files | Purpose |
|----------|-------|---------|
| **Game Systems** | ~35 | Test core game mechanics (combat, inventory, spatial) |
| **TUI Client** | ~5 | Test text user interface components |
| **Components** | ~20 | Test entity components (doors, items, rooms) |
| **Commands** | ~10 | Test command parsing and execution |
| **Integration** | ~8 | Test system interactions |

---

## Test Categories

### 1. Unit Tests (pytest marker: `@pytest.mark.unit`)

Test individual components in isolation.

**Examples:**
- `test_accounts.py` — Account creation and authentication
- `test_aliases.py` — Command alias system
- `test_doors.py` — Door component behavior
- `test_inventory_sync.py` — Inventory synchronization

**Characteristics:**
- Fast execution (<100ms per test)
- Use mocking for external dependencies
- Test single responsibility
- No database or network calls

### 2. Integration Tests (pytest marker: `@pytest.mark.integration`)

Test interactions between multiple components.

**Examples:**
- `test_botany_kitchen.py` — Botany + Kitchen system integration
- `test_cyborg_med_integration.py` — Cyborg + Medical system
- `test_genetic_med_integration.py` — Genetics + Medical system
- `test_robotics_ai_integration.py` — Robotics + AI system

**Characteristics:**
- Medium execution time (100ms-1s)
- Test component interactions
- May use test database
- Verify data flow between systems

### 3. End-to-End Tests (pytest marker: `@pytest.mark.e2e`)

Test complete user workflows.

**Examples:**
- `test_tui_playwright.py` — Full TUI workflows with Playwright
- Manual testing scenarios

**Characteristics:**
- Slow execution (>1s)
- Require running server
- Test complete user journeys
- May be skipped in CI

### 4. Async Tests (pytest marker: `@pytest.mark.asyncio`)

Test asynchronous code (WebSocket, event loops).

**Examples:**
- `test_tui_client.py` — Async GameClient tests
- `test_tui_logging.py` — Async logging tests

**Characteristics:**
- Use asyncio event loop
- Test async/await patterns
- Verify concurrent behavior
- Use AsyncMock for async methods

---

## Naming Conventions

### File Naming

```
test_<module_or_feature>.py
```

**Examples:**
- `test_doors.py` — Tests for door components
- `test_combat_system.py` — Tests for combat mechanics
- `test_tui_client.py` — Tests for TUI client

### Test Function Naming

```python
def test_<what>_<when>_<expected>():
    """Descriptive docstring."""
```

**Examples:**
```python
def test_door_opens_when_unlocked():
    """Door should open when it's unlocked."""

def test_command_fails_when_invalid_syntax():
    """Command parsing should fail with invalid syntax."""

def test_player_takes_damage_when_attacked():
    """Player health should decrease when attacked."""
```

### Test Class Naming

```python
class Test<Component>:
    """Test cases for <Component>."""
```

**Examples:**
```python
class TestGameClient:
    """Test cases for GameClient."""

class TestDoorComponent:
    """Test cases for Door component."""
```

---

## Testing Patterns

### 1. Arrange-Act-Assert (AAA)

**Structure:**
```python
def test_example():
    # Arrange: Set up test data and mocks
    player = Player("test_user")
    item = Item("wrench")
    
    # Act: Execute the code being tested
    player.add_item(item)
    
    # Assert: Verify the expected outcome
    assert item in player.inventory
    assert len(player.inventory) == 1
```

### 2. Given-When-Then (BDD Style)

**Structure:**
```python
def test_player_equips_armor():
    """
    Given a player with armor in inventory
    When the player equips the armor
    Then the armor should be marked as equipped
    """
    # Given
    player = Player("test_user")
    armor = Item("helmet", type="armor")
    player.add_item(armor)
    
    # When
    player.equip(armor)
    
    # Then
    assert armor.equipped is True
    assert player.equipped_armor == armor
```

### 3. Parametrized Tests

**Test multiple scenarios:**
```python
@pytest.mark.parametrize("command,expected", [
    ("look", "You look around"),
    ("north", "You move north"),
    ("inventory", "Your inventory:"),
])
def test_command_responses(command, expected):
    """Test various command responses."""
    result = parse_command(command)
    assert expected in result
```

### 4. Fixture-Based Setup

**Reusable test setup:**
```python
@pytest.fixture
def game_world():
    """Create a test game world."""
    world = World()
    world.add_room("test_room")
    return world

def test_world_has_room(game_world):
    """World should contain the test room."""
    assert "test_room" in game_world.rooms
```

---

## Fixtures and Mocking

### Shared Fixtures (conftest.py)

#### event_loop
Creates an asyncio event loop for async tests.

```python
@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

#### mock_websocket
Provides a mocked WebSocket connection.

```python
@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket connection."""
    ws = AsyncMock()
    ws.send = AsyncMock()
    ws.recv = AsyncMock()
    ws.close = AsyncMock()
    ws.closed = False
    return ws
```

#### mock_app
Provides a mocked Textual app instance.

```python
@pytest.fixture
def mock_app():
    """Create a mock Textual app instance."""
    app = Mock()
    app.on_login_success = AsyncMock()
    app.notify = Mock()
    app.push_screen = Mock()
    app.pop_screen = Mock()
    app.exit = Mock()
    return app
```

#### sample_messages
Provides realistic test data for WebSocket messages.

```python
@pytest.fixture
def sample_messages():
    """Provide sample WebSocket messages for testing."""
    return {
        "response": {"type": "response", "message": "..."},
        "system": {"type": "system", "message": "..."},
        "error": {"type": "error", "message": "..."},
        # ... more message types
    }
```

#### sample_commands
Provides common game commands for testing.

```python
@pytest.fixture
def sample_commands():
    """Provide sample game commands for testing."""
    return ["look", "inventory", "north", "south", ...]
```

### Mocking Patterns

#### Mock Functions

```python
from unittest.mock import Mock, patch

def test_function_call():
    mock_func = Mock(return_value="test")
    result = mock_func()
    assert result == "test"
    mock_func.assert_called_once()
```

#### Mock Async Functions

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_function():
    mock_async = AsyncMock(return_value="test")
    result = await mock_async()
    assert result == "test"
    mock_async.assert_awaited_once()
```

#### Patch External Dependencies

```python
@patch('module.external_api_call')
def test_with_patch(mock_api):
    mock_api.return_value = {"status": "success"}
    result = function_that_calls_api()
    assert result["status"] == "success"
```

#### Mock Object Attributes

```python
def test_object_attributes():
    mock_player = Mock()
    mock_player.health = 100
    mock_player.name = "TestPlayer"
    
    assert mock_player.health == 100
    assert mock_player.name == "TestPlayer"
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_doors.py
```

### Run Specific Test Function

```bash
pytest tests/test_doors.py::test_door_opens_when_unlocked
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only async tests
pytest -m asyncio

# Run only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"
```

### Run with Coverage

```bash
# Basic coverage
pytest --cov=.

# Coverage with HTML report
pytest --cov=. --cov-report=html

# Coverage for specific module
pytest --cov=tui_client --cov-report=term-missing
```

### Run with Verbose Output

```bash
# Show test names
pytest -v

# Show full test output
pytest -vv

# Show print statements
pytest -s
```

### Run Failed Tests Only

```bash
# Run last failed tests
pytest --lf

# Run failed first, then others
pytest --ff
```

### Run in Parallel

```bash
# Run with 4 processes (requires pytest-xdist)
pytest -n 4

# Run with auto-detection
pytest -n auto
```

---

## Best Practices

### 1. Test Independence

**DO**: Each test should run independently
```python
def test_independent():
    player = Player("test")  # Fresh instance each test
    assert player.health == 100
```

**DON'T**: Tests should not depend on execution order
```python
# Bad: Depends on previous test
def test_dependent():
    assert player.health == 50  # Assumes previous test modified player
```

### 2. Use Descriptive Names

**DO**: Clear, descriptive test names
```python
def test_player_health_decreases_when_damaged():
    """Player health should decrease when taking damage."""
```

**DON'T**: Vague test names
```python
def test_1():
    """Test."""
```

### 3. One Assertion Per Concept

**DO**: Test one thing, assert multiple related aspects
```python
def test_player_equips_armor():
    player.equip(armor)
    assert armor.equipped is True
    assert player.equipped_armor == armor
    assert armor.durability == 100
```

**DON'T**: Test multiple unrelated things
```python
def test_everything():
    # Tests equipment, movement, combat, inventory...
```

### 4. Use Fixtures for Setup

**DO**: Reusable fixtures
```python
@pytest.fixture
def game_world():
    return World()

def test_with_world(game_world):
    assert game_world is not None
```

**DON'T**: Duplicate setup code
```python
def test_1():
    world = World()  # Repeated in every test
    
def test_2():
    world = World()  # Same setup
```

### 5. Mock External Dependencies

**DO**: Mock external services
```python
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    result = fetch_data()
    assert result["data"] == "test"
```

**DON'T**: Call real external services
```python
def test_real_api():
    result = requests.get("https://api.example.com")  # Bad: real network call
```

### 6. Test Error Cases

**DO**: Test both success and failure
```python
def test_door_opens_when_unlocked():
    door.locked = False
    assert door.open() is True

def test_door_fails_when_locked():
    door.locked = True
    with pytest.raises(DoorLockedError):
        door.open()
```

### 7. Keep Tests Fast

**DO**: Use mocks for speed
```python
def test_fast():
    mock_db = Mock()
    result = function_using_db(mock_db)
```

**DON'T**: Real database in unit tests
```python
def test_slow():
    db = connect_to_real_database()  # Slow
    result = function_using_db(db)
```

### 8. Clear Arrange-Act-Assert

**DO**: Separate phases clearly
```python
def test_inventory_add():
    # Arrange
    player = Player("test")
    item = Item("wrench")
    
    # Act
    player.add_item(item)
    
    # Assert
    assert item in player.inventory
```

### 9. Use Parametrize for Similar Tests

**DO**: Parametrize multiple scenarios
```python
@pytest.mark.parametrize("health,expected", [
    (100, "Healthy"),
    (50, "Injured"),
    (10, "Critical"),
])
def test_health_status(health, expected):
    assert get_status(health) == expected
```

**DON'T**: Duplicate test functions
```python
def test_healthy():
    assert get_status(100) == "Healthy"
    
def test_injured():
    assert get_status(50) == "Injured"
    
# etc...
```

### 10. Document Complex Tests

**DO**: Add docstrings and comments
```python
def test_complex_interaction():
    """
    Test the complex interaction between player, door, and room.
    
    This verifies that:
    1. Player can see the door
    2. Player can open unlocked door
    3. Player moves through door to new room
    4. Door state updates in both rooms
    """
    # Setup: Create connected rooms
    room1, room2 = create_connected_rooms()
    
    # ... test implementation
```

---

## Test Coverage Guidelines

### Target Coverage

- **Overall**: Aim for 70%+ code coverage
- **Critical Systems**: 90%+ coverage (authentication, combat, economy)
- **TUI Components**: 80%+ coverage (screens, client)
- **Utilities**: 60%+ coverage (helpers, formatters)

### Coverage Commands

```bash
# Generate coverage report
pytest --cov=. --cov-report=term-missing

# Generate HTML report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Show missing lines
pytest --cov=. --cov-report=term-missing

# Fail if below threshold
pytest --cov=. --cov-fail-under=70
```

### What to Test

**High Priority:**
- User authentication and authorization
- Command parsing and execution
- Combat and damage calculations
- Inventory management
- Economy and trading
- Door and access control

**Medium Priority:**
- TUI screen rendering
- WebSocket message handling
- Room and location management
- Item interactions
- NPC behaviors

**Lower Priority:**
- Formatting utilities
- Logging helpers
- Debug commands
- Admin-only features

---

## Common Testing Scenarios

### Testing Async Code

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    mock_ws = AsyncMock()
    mock_ws.send.return_value = None
    
    await send_message(mock_ws, "test")
    
    mock_ws.send.assert_awaited_once_with("test")
```

### Testing Exceptions

```python
import pytest

def test_raises_exception():
    """Test that function raises expected exception."""
    with pytest.raises(ValueError, match="Invalid input"):
        process_invalid_input("bad_data")
```

### Testing WebSocket Messages

```python
def test_websocket_message_handling(mock_websocket, sample_messages):
    """Test handling of WebSocket messages."""
    client = GameClient(mock_websocket)
    
    # Simulate receiving message
    await client.handle_message(sample_messages["response"])
    
    # Verify message was processed
    assert client.last_response == "You look around the room."
```

### Testing TUI Components

```python
from textual.widgets import Static

def test_tui_widget_render():
    """Test TUI widget rendering."""
    widget = Static("Test content")
    
    # Verify content
    assert widget.renderable == "Test content"
    
    # Update content
    widget.update("New content")
    assert widget.renderable == "New content"
```

---

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Pull request creation
- Push to main branch
- Manual workflow dispatch

### CI Configuration

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: pytest --cov=. --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

---

## Additional Resources

- [TESTING_GUIDE.md](TESTING_GUIDE.md) — Comprehensive testing guide
- [README_TUI_TESTS.md](../tests/README_TUI_TESTS.md) — TUI-specific tests
- [conftest.py](../tests/conftest.py) — Shared fixtures
- [pytest.ini](../pytest.ini) — Pytest configuration

---

**Last Updated**: 2026-01-13  
**Maintained By**: Development Team  
**Related**: BATCH-004 Documentation Enhancement
