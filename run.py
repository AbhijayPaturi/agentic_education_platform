#!/usr/bin/env python3
"""Entry point for running the application from project root."""

import sys
from pathlib import Path

# Add project root to path so src module can be imported
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Run the application
from src.app.run import main  # noqa: E402

if __name__ == "__main__":
    main()
