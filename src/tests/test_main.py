"""Tests for main application logic."""

import pytest
from unittest.mock import patch, MagicMock
from src.app.main import (
    get_user_input,
    parse_topics_from_output,
    get_user_approval,
    process_topic,
    main
)


@pytest.fixture
def mock_crew_output():
    """Create a mock CrewOutput for testing."""
    output = MagicMock()
    output.raw = "Test raw output"
    output.json_dict = {
        'topics': [
            {'order': 1, 'topic_name': 'Topic 1'},
            {'order': 2, 'topic_name': 'Topic 2'}
        ]
    }
    return output


class TestParseTopicsFromOutput:
    """Test topic parsing from curriculum output."""
    
    def test_parse_structured_json_output(self, mock_crew_output):
        """Test parsing from structured JSON output."""
        mock_crew = MagicMock()
        mock_crew.get_task_output.return_value = mock_crew_output
        
        topics = parse_topics_from_output(mock_crew)
        
        assert len(topics) == 2
        assert 'Topic 1' in topics
        assert 'Topic 2' in topics
    
    def test_parse_markdown_format(self):
        """Test parsing from markdown format."""
        mock_crew = MagicMock()
        mock_output = MagicMock()
        del mock_output.json_dict
        mock_output.raw = """
        1. **Machine Learning** (5 days)
        2. **Deep Learning** (6 days)
        3. **Natural Language Processing** (4 days)
        """
        mock_crew.get_task_output.return_value = mock_output
        
        topics = parse_topics_from_output(mock_crew)
        
        assert len(topics) == 3
        assert 'Machine Learning' in topics
    
    def test_parse_no_output(self):
        """Test parsing when no output available."""
        mock_crew = MagicMock()
        mock_crew.get_task_output.return_value = None
        
        topics = parse_topics_from_output(mock_crew)
        
        assert topics == []
    
    def test_parse_malformed_output(self):
        """Test parsing malformed output."""
        mock_crew = MagicMock()
        mock_output = MagicMock()
        del mock_output.json_dict
        mock_output.raw = "Random text without proper formatting"
        mock_crew.get_task_output.return_value = mock_output
        
        topics = parse_topics_from_output(mock_crew)
        
        # Should return empty list or handle gracefully
        assert isinstance(topics, list)


class TestGetUserApproval:
    """Test user approval dialog."""
    
    @patch('builtins.input', return_value='yes')
    def test_user_approves(self, mock_input):
        """Test user approving curriculum."""
        topics = ['Topic 1', 'Topic 2']
        result = get_user_approval(topics)
        assert result is True
    
    @patch('builtins.input', return_value='no')
    def test_user_rejects(self, mock_input):
        """Test user rejecting curriculum."""
        topics = ['Topic 1', 'Topic 2']
        result = get_user_approval(topics)
        assert result is False
    
    @patch('builtins.input', side_effect=['maybe', 'invalid', 'yes'])
    def test_user_invalid_then_valid(self, mock_input):
        """Test handling invalid input then valid."""
        topics = ['Topic 1']
        result = get_user_approval(topics)
        assert result is True
        assert mock_input.call_count == 3
    
    @patch('builtins.input', return_value='y')
    def test_user_shorthand_yes(self, mock_input):
        """Test accepting shorthand 'y' for yes."""
        topics = ['Topic 1']
        result = get_user_approval(topics)
        assert result is True
    
    @patch('builtins.input', return_value='n')
    def test_user_shorthand_no(self, mock_input):
        """Test accepting shorthand 'n' for no."""
        topics = ['Topic 1']
        result = get_user_approval(topics)
        assert result is False


class TestProcessTopic:
    """Test single topic processing."""
    
    @patch('src.app.main.ContentGenerationCrew')
    @patch('src.app.main.save_content_outputs')
    def test_process_topic_success(self, mock_save, mock_crew_class):
        """Test successful topic processing."""
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = "Success"
        mock_crew_class.return_value = mock_crew
        
        result = process_topic("Python Basics", 1, 5)
        
        assert result is True
        mock_crew_class.assert_called_once_with("Python Basics")
        mock_crew.kickoff.assert_called_once()
        mock_save.assert_called_once()
    
    @patch('src.app.main.ContentGenerationCrew')
    def test_process_topic_failure(self, mock_crew_class):
        """Test topic processing with exception."""
        mock_crew_class.side_effect = Exception("Test error")
        
        result = process_topic("Bad Topic", 1, 1)
        
        assert result is False
    
    @patch('src.app.main.ContentGenerationCrew')
    @patch('src.app.main.save_content_outputs')
    def test_process_topic_with_special_chars(self, mock_save, mock_crew_class):
        """Test processing topic with special characters."""
        mock_crew = MagicMock()
        mock_crew_class.return_value = mock_crew
        
        result = process_topic("C++/C# Programming!", 1, 1)
        
        assert result is True


class TestGetUserInput:
    """Test user input gathering."""
    
    @patch('builtins.input', side_effect=['Alice', 'Data Scientist'])
    def test_get_user_input_normal(self, mock_input):
        """Test normal user input."""
        name, goal = get_user_input()
        
        assert name == 'Alice'
        assert goal == 'Data Scientist'
    
    @patch('builtins.input', side_effect=['', 'Bob', 'Become a software engineer'])
    def test_get_user_input_empty_name_retry(self, mock_input):
        """Test retry on empty name."""
        name, goal = get_user_input()
        
        assert name == 'Bob'
        assert goal == 'Become a software engineer'
        assert mock_input.call_count == 3
    
    @patch('builtins.input', side_effect=['Carol', '', 'ML Engineer'])
    def test_get_user_input_empty_goal_retry(self, mock_input):
        """Test retry on empty goal."""
        name, goal = get_user_input()
        
        assert name == 'Carol'
        assert goal == 'ML Engineer'
    
    @patch('builtins.input', side_effect=['  Dave  ', '  Become a DevOps Engineer  '])
    def test_get_user_input_strips_whitespace(self, mock_input):
        """Test that input is stripped of whitespace."""
        name, goal = get_user_input()
        
        assert name == 'Dave'
        assert goal == 'Become a DevOps Engineer'


class TestMainFunction:
    """Test main application entry point."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test123'})
    @patch('builtins.input', side_effect=['Alice', 'Become a machine learning engineer', 'yes'])
    @patch('src.app.main.CurriculumCrew')
    @patch('src.app.main.ContentGenerationCrew')
    @patch('src.app.main.save_content_outputs')
    def test_main_successful_flow(self, mock_save, mock_content_crew, mock_curr_crew, mock_input):
        """Test successful main execution flow."""
        # Setup curriculum crew
        mock_curr = MagicMock()
        mock_output = MagicMock()
        mock_output.json_dict = {
            'topics': [{'order': 1, 'topic_name': 'Topic 1'}]
        }
        mock_curr.get_task_output.return_value = mock_output
        mock_curr_crew.return_value = mock_curr
        
        # Setup content crew
        mock_content = MagicMock()
        mock_content_crew.return_value = mock_content
        
        # Main should complete without raising
        main()
        
        # Verify crews were called
        mock_curr_crew.assert_called_once()
        mock_content_crew.assert_called()
    
    @patch.dict('os.environ', {}, clear=True)
    def test_main_missing_api_key(self):
        """Test main exits when API key is missing."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'invalid-key'})
    def test_main_invalid_api_key_format(self):
        """Test main validates API key format."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test123'})
    @patch('builtins.input', side_effect=['Bob', 'Become a data scientist', 'no'])
    @patch('src.app.main.CurriculumCrew')
    def test_main_user_rejects_curriculum(self, mock_curr_crew, mock_input):
        """Test main exits when user rejects curriculum."""
        mock_curr = MagicMock()
        mock_output = MagicMock()
        mock_output.json_dict = {
            'topics': [{'order': 1, 'topic_name': 'Topic 1'}]
        }
        mock_curr.get_task_output.return_value = mock_output
        mock_curr_crew.return_value = mock_curr
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test123'})
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_main_handles_keyboard_interrupt(self, mock_input):
        """Test main handles Ctrl+C gracefully."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
