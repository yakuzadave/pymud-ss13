# PyMUD-SS13 Examples

This directory contains example scripts demonstrating various features of PyMUD-SS13.

## Available Examples

### logging_demo.py

Demonstrates the enhanced TUI logging system with examples of:
- Basic logging at different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Contextual logging with user actions
- Exception logging with stack traces
- Conditional logging for performance
- Performance metrics logging
- Dynamic log level changes
- Log cleanup functionality

**Run it:**
```bash
python examples/logging_demo.py
```

**Output:**
- Console output showing logging demonstrations
- Log files in `logs/tui/` directory

## Running Examples

From the project root directory:

```bash
# Make sure you're in the project root
cd /path/to/pymud-ss13

# Run an example
python examples/logging_demo.py
```

## Creating New Examples

When creating new example scripts:

1. Add a descriptive header comment
2. Include usage instructions in the docstring
3. Make the script executable: `chmod +x examples/your_script.py`
4. Add an entry to this README
5. Test the script from the project root

## Example Template

```python
#!/usr/bin/env python3
"""
Brief description of what this example demonstrates.

Usage:
    python examples/your_example.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Your imports here
from tui_client import something


def main():
    """Main function."""
    print("Your example code here")


if __name__ == "__main__":
    main()
```

## Additional Resources

- [Testing Guide](../docs/TESTING_GUIDE.md)
- [Logging Guide](../docs/LOGGING_GUIDE.md)
- [TUI Documentation](../docs/TEXTUAL_TUI_IMPLEMENTATION.md)
- [Main README](../README.md)
