"""Tests for configuration module."""

import pytest
from pathlib import Path
from src.config.config import Config


@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock the OpenAI API key for testing."""
    monkeypatch.setattr(Config, 'OPENAI_API_KEY', 'sk-test-api-key-12345')
    return 'sk-test-api-key-12345'


class TestConfig:
    """Test configuration management."""
    
    def test_config_has_required_attributes(self):
        """Verify Config has all required class attributes."""
        assert hasattr(Config, 'OPENAI_API_KEY')
        assert hasattr(Config, 'DEFAULT_MODEL')
        assert hasattr(Config, 'OUTPUT_DIR')
        assert hasattr(Config, 'VERBOSE')
    
    def test_default_model_is_configured(self):
        """Verify a default model is set and configurable via OPENAI_MODEL."""
        assert isinstance(Config.DEFAULT_MODEL, str)
        assert Config.DEFAULT_MODEL
    
    def test_output_dir_is_path(self):
        """Verify output directory is a Path object."""
        assert isinstance(Config.OUTPUT_DIR, Path)
    
    def test_verbose_is_boolean(self):
        """Verify verbose flag is boolean."""
        assert isinstance(Config.VERBOSE, bool)
    
    def test_get_output_path_creates_directory(self, mock_output_dir):
        """Test output path generation creates directories."""
        output_path = Config.get_output_path('Test Topic')
        
        assert output_path.exists()
        assert output_path.is_dir()
        assert 'Test_Topic' in str(output_path)
    
    def test_get_output_path_with_lesson_number(self, mock_output_dir):
        """Test output path with lesson number."""
        output_path = Config.get_output_path('Python Basics', lesson_number=3)
        
        assert output_path.exists()
        assert 'lesson_3' in str(output_path)
    
    def test_get_output_path_sanitizes_special_chars(self, mock_output_dir):
        """Test path sanitization of special characters."""
        output_path = Config.get_output_path('C++/C# Programming!')
        
        assert output_path.exists()
        # Special chars should be replaced with underscores
        assert '!' not in str(output_path)
        assert '/' not in output_path.name
    
    def test_validate_raises_without_api_key(self, monkeypatch):
        """Test validation fails without API key."""
        monkeypatch.setattr(Config, 'OPENAI_API_KEY', None)
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            Config.validate()
    
    def test_validate_creates_output_dir(self, mock_output_dir, mock_api_key):
        """Test validation creates output directory."""
        Config.validate()
        
        assert mock_output_dir.exists()
