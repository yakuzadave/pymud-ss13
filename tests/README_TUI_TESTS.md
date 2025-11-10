# TUI Client Test Suite

This directory contains comprehensive tests for the PyMUD-SS13 Textual TUI client.

## Test Files

### test_tui_client.py

Main test file containing:

- **TestGameClient**: Unit tests for the WebSocket client
  - Connection management
  - Message handling and routing
  - Handler registration/unregistration
  - State caching (location, inventory, map)
  - Async handler support

- **TestPyMUDApp**: Tests for the main application
  - Initialization
  - Server URL configuration
  - Key bindings

- **TestLoginScreen**: Tests for the login screen
  - Initialization
  - Form handling

- **TestGameScreen**: Tests for the main game view
  - Initialization
  - Command history
  - Key bindings
  - Message handlers

- **TestInventoryScreen**: Tests for the inventory view
  - Initialization
  - Item management
  - Equipment handling
  - Key bindings

- **TestMapScreen**: Tests for the map view
  - Initialization
  - Grid creation
  - Navigation
  - Key bindings

- **TestHelpScreen**: Tests for the help view
  - Initialization

- **TestIntegration**: Integration tests
  - Message routing between components
  - Async handler support
  - State caching across screens

- **TestPerformance**: Performance benchmarks
  - Message handling speed
  - State access performance

### conftest.py

Shared pytest fixtures:

- `event_loop`: Async event loop for testing
- `mock_websocket`: Mock WebSocket connection
- `mock_app`: Mock Textual app instance
- `sample_messages`: Sample WebSocket messages
- `sample_commands`: Sample game commands

## Running Tests

### Run All TUI Tests

```bash
pytest tests/test_tui_client.py -v
```

### Run Specific Test Classes

```bash
# Test only GameClient
pytest tests/test_tui_client.py::TestGameClient -v

# Test only screens
pytest tests/test_tui_client.py::TestGameScreen -v
pytest tests/test_tui_client.py::TestInventoryScreen -v
pytest tests/test_tui_client.py::TestMapScreen -v
```

### Run Specific Tests

```bash
# Test message handling
pytest tests/test_tui_client.py::TestGameClient::test_handle_message_location -v

# Test performance
pytest tests/test_tui_client.py::TestPerformance -v
```

### Run with Coverage

```bash
pytest tests/test_tui_client.py --cov=tui_client --cov-report=html
```

### Run Async Tests Only

```bash
pytest tests/test_tui_client.py -m asyncio -v
```

## Test Coverage

The test suite covers:

- ✅ GameClient initialization and configuration
- ✅ WebSocket message handling
- ✅ Message type routing
- ✅ Handler registration system
- ✅ State caching (location, inventory, map, status)
- ✅ Screen initialization
- ✅ Key bindings for all views
- ✅ Command history management
- ✅ Inventory item handling
- ✅ Map grid creation and updates
- ✅ Async handler support
- ✅ Integration between components
- ✅ Performance benchmarks

## Test Structure

### Unit Tests

Test individual components in isolation:
- GameClient methods
- Screen initialization
- Message handlers
- State getters

### Integration Tests

Test interaction between components:
- Message routing to screens
- Handler registration and calling
- State sharing

### Performance Tests

Benchmark critical operations:
- Message handling speed
- State access performance
- Handler execution time

## Writing New Tests

### Adding a New Test

1. Add to the appropriate test class in `test_tui_client.py`
2. Use fixtures from `conftest.py` for common setup
3. Follow the naming convention: `test_<what_is_being_tested>`
4. Use descriptive docstrings

Example:

```python
def test_new_feature(self, game_client):
    """Test that the new feature works correctly."""
    result = game_client.new_feature()
    assert result is True
```

### Testing Async Code

Use the `@pytest.mark.asyncio` decorator:

```python
@pytest.mark.asyncio
async def test_async_feature(self, game_client):
    """Test async functionality."""
    result = await game_client.async_method()
    assert result is not None
```

### Using Mocks

Mock external dependencies:

```python
from unittest.mock import Mock, AsyncMock

def test_with_mock(self):
    """Test using mocks."""
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()

    # Use the mock in your test
    await mock_ws.send("test")
    mock_ws.send.assert_called_once()
```

## Fixtures

### Available Fixtures

- `event_loop`: For async tests
- `mock_websocket`: Mock WebSocket connection
- `mock_app`: Mock Textual app
- `sample_messages`: Pre-defined test messages
- `sample_commands`: Common game commands
- `sample_location_data`: Sample location info
- `sample_inventory_data`: Sample inventory
- `sample_map_data`: Sample map grid

### Creating New Fixtures

Add to `conftest.py`:

```python
@pytest.fixture
def my_fixture():
    """Description of the fixture."""
    data = setup_data()
    yield data
    cleanup_data(data)
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# .github/workflows/tui-tests.yml
- name: Run TUI Tests
  run: |
    pip install pytest pytest-asyncio pytest-cov
    pytest tests/test_tui_client.py -v --cov=tui_client
```

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. You're in the project root directory
2. The `tui_client` package is in your Python path
3. All dependencies are installed: `pip install -r requirements.txt`

### Async Test Failures

If async tests fail:
1. Make sure `pytest-asyncio` is installed
2. Check that you're using `@pytest.mark.asyncio`
3. Verify event loop fixture is working

### Mock Issues

If mocks aren't working:
1. Check that you're importing from `unittest.mock`
2. Verify the mock is created before use
3. Use `AsyncMock` for async functions

## Performance Benchmarks

Expected performance targets:

- Message handling: < 1 second for 100 messages with 10 handlers
- State access: < 0.1 seconds for 4000 state accesses
- Handler execution: < 0.01 seconds per handler

Run benchmarks:

```bash
pytest tests/test_tui_client.py::TestPerformance -v --durations=10
```

## Contributing

When adding new TUI features:

1. Write tests first (TDD approach)
2. Ensure all tests pass before committing
3. Add integration tests for new components
4. Update this README if adding new test categories
5. Maintain > 80% code coverage

## Related Documentation

- [TUI Client README](../tui_client/README.md)
- [TUI Implementation Guide](../docs/TEXTUAL_TUI_IMPLEMENTATION.md)
- [Main Project Tests](../tests/)

---

**Last Updated**: 2025-11-10
**Test Count**: 40+ tests
**Coverage Target**: > 80%
