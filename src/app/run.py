#!/usr/bin/env python3
"""Application launcher.

SSL/telemetry configuration is centralized in ``src.config.config`` and applied
at import time. To bypass TLS verification on corporate networks that perform
TLS interception, set ``DISABLE_SSL_VERIFY=true`` in your ``.env`` (off by
default so the application is secure out of the box).
"""

import sys
from pathlib import Path

# Add project root to path so the ``src`` package is importable.
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importing main triggers src.config.config, which configures SSL/telemetry
# before any network client is created.
from src.app.main import main  # noqa: E402

if __name__ == "__main__":
    main()
