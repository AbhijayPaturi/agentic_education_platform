"""Shared pytest fixtures used across multiple test modules.

This conftest.py contains only fixtures that are used by multiple test files.
Test-specific fixtures should be defined in the individual test files.
"""

import pytest


@pytest.fixture
def mock_output_dir(tmp_path, monkeypatch):
    """Create a temporary output directory and configure Config to use it.
    
    Used by: test_config.py, test_agents.py, test_utils.py
    """
    from src.config.config import Config
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    monkeypatch.setattr(Config, 'OUTPUT_DIR', output_dir)
    return output_dir
