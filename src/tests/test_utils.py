"""Tests for utility functions."""

import pytest
from unittest.mock import MagicMock
from src.utils.output_utils import (
    print_banner,
    print_section,
    format_lesson_plan,
    format_slides,
    format_videos,
    format_quiz,
    format_quiz_answer_key,
    save_content_outputs
)


@pytest.fixture
def mock_lesson_plan_data():
    """Create mock lesson plan data dictionary."""
    return {
        'topic': 'Python Basics',
        'overview': 'Introduction to Python programming',
        'learning_objectives': [
            {'objective': 'Understand variables', 'blooms_level': 'Remember'}
        ],
        'lessons': [
            {
                'lesson_number': 1,
                'title': 'Variables',
                'learning_objective': 'Learn variables',
                'duration_minutes': 60,
                'key_concepts': ['int', 'str'],
                'teaching_approach': 'Hands-on',
                'resources_needed': ['IDE']
            }
        ],
        'assessment_strategy': 'Quiz and projects',
        'estimated_total_time': 60
    }


@pytest.fixture
def mock_slides_data():
    """Create mock slides data dictionary."""
    return {
        'topic': 'Python Basics',
        'slides': [
            {
                'slide_number': i,
                'title': f'Slide {i}',
                'content_type': 'content',
                'content': f'Content {i}',
                'speaker_notes': f'Notes {i}'
            }
            for i in range(1, 11)
        ],
        'total_slides': 10,
        'design_notes': 'Use clear visuals'
    }


@pytest.fixture
def mock_videos_data():
    """Create mock videos data dictionary."""
    return {
        'topic': 'Python Basics',
        'videos': [
            {
                'title': f'Video {i}',
                'hypothetical_url': f'http://example.com/v{i}',
                'description': f'Tutorial {i}',
                'estimated_duration': '10 minutes',
                'difficulty_level': 'Beginner',
                'key_topics_covered': ['topic'],
                'suggested_viewing_order': i,
                'recommended_channel': 'freeCodeCamp',
                'search_query': f'tutorial {i}',
                'rationale': f'Useful for topic {i}'
            }
            for i in range(1, 6)
        ],
        'viewing_guide': 'Watch in order'
    }


@pytest.fixture
def mock_quiz_data():
    """Create mock quiz data dictionary."""
    return {
        'topic': 'Python Basics',
        'quiz_type': 'formative',
        'questions': [
            {
                'question_number': i,
                'question_type': 'multiple_choice',
                'difficulty': 'easy',
                'question': f'Question {i}?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A',
                'explanation': f'Explanation {i}',
                'learning_objective_tested': f'Objective {i}'
            }
            for i in range(1, 11)
        ],
        'total_points': 100,
        'time_limit_minutes': 30,
        'passing_score': 70,
        'study_tips': 'Review materials'
    }


class TestPrintFunctions:
    """Test printing utility functions."""
    
    def test_print_banner_output(self, capsys):
        """Test print_banner produces output."""
        print_banner("Test Banner")
        captured = capsys.readouterr()
        assert "Test Banner" in captured.out
        assert "=" in captured.out
    
    def test_print_banner_custom_char(self, capsys):
        """Test print_banner with custom character."""
        print_banner("Test", char="-")
        captured = capsys.readouterr()
        assert "Test" in captured.out
        assert "-" in captured.out
    
    def test_print_section_output(self, capsys):
        """Test print_section produces output."""
        print_section("Test Section")
        captured = capsys.readouterr()
        assert "Test Section" in captured.out
        assert "►" in captured.out or "▶" in captured.out


class TestFormatLessonPlan:
    """Test lesson plan formatting."""
    
    def test_format_lesson_plan_basic(self, mock_lesson_plan_data):
        """Test basic lesson plan formatting."""
        result = format_lesson_plan(mock_lesson_plan_data)
        
        assert 'Python Basics' in result
        assert 'Introduction to Python' in result
        assert 'Variables' in result
        assert '60 minutes' in result
    
    def test_format_lesson_plan_empty_objectives(self):
        """Test formatting with empty objectives."""
        data = {
            'topic': 'Test',
            'overview': 'Test',
            'learning_objectives': [],
            'lessons': [],
            'assessment_strategy': 'None',
            'estimated_total_time': 0
        }
        
        result = format_lesson_plan(data)
        assert 'Test' in result
    
    def test_format_lesson_plan_missing_resources(self):
        """Test formatting lesson without resources_needed."""
        data = {
            'topic': 'Test',
            'overview': 'Test',
            'learning_objectives': [],
            'lessons': [
                {
                    'lesson_number': 1,
                    'title': 'Test',
                    'learning_objective': 'Test',
                    'duration_minutes': 30,
                    'key_concepts': ['test'],
                    'teaching_approach': 'Test'
                }
            ],
            'assessment_strategy': 'Test',
            'estimated_total_time': 30
        }
        
        result = format_lesson_plan(data)
        assert 'Test' in result


class TestFormatSlides:
    """Test slides formatting."""
    
    def test_format_slides_basic(self, mock_slides_data):
        """Test basic slides formatting."""
        result = format_slides(mock_slides_data)
        
        assert 'Python' in result
        assert 'Slide 1' in result
        assert 'Use clear visuals' in result
    
    def test_format_slides_no_speaker_notes(self):
        """Test formatting slides without speaker notes."""
        data = {
            'topic': 'Test',
            'total_slides': 1,
            'slides': [
                {
                    'title': 'Test',
                    'content_type': 'text',
                    'content': 'Content'
                }
            ],
            'design_notes': 'Notes'
        }
        
        result = format_slides(data)
        assert 'Test' in result


class TestFormatVideos:
    """Test video resources formatting."""
    
    def test_format_videos_basic(self, mock_videos_data):
        """Test basic video formatting."""
        result = format_videos(mock_videos_data)
        
        assert 'Python' in result
        assert 'Video 1' in result
        assert 'Beginner' in result
    
    def test_format_videos_empty_list(self):
        """Test formatting with no videos."""
        data = {
            'topic': 'Test',
            'videos': [],
            'viewing_guide': 'None'
        }
        
        result = format_videos(data)
        assert 'Test' in result


class TestFormatQuiz:
    """Test quiz formatting."""
    
    def test_format_quiz_basic(self, mock_quiz_data):
        """Test basic quiz formatting."""
        result = format_quiz(mock_quiz_data)
        
        assert 'Python' in result
        assert 'Question 1' in result
        assert '70%' in result
        assert '**Answer**' not in result

        answer_key = format_quiz_answer_key(mock_quiz_data)
        assert '# Answer Key: Python Basics' in answer_key
        assert '**Answer**: A' in answer_key
        assert '**Explanation**: Explanation 1' in answer_key
    
    def test_format_quiz_no_options(self):
        """Test formatting quiz with no options (short answer)."""
        data = {
            'topic': 'Test',
            'quiz_type': 'test',
            'total_points': 10,
            'time_limit_minutes': 30,
            'passing_score': 60,
            'questions': [
                {
                    'question_number': 1,
                    'difficulty': 'medium',
                    'question_type': 'short_answer',
                    'question': 'Explain',
                    'correct_answer': 'Answer',
                    'explanation': 'Explanation',
                    'learning_objective_tested': 'Understanding'
                }
            ],
            'study_tips': 'Study'
        }
        
        result = format_quiz(data)
        assert 'Explain' in result


class TestSaveContentOutputs:
    """Test saving content outputs."""
    
    def test_save_content_outputs_creates_files(self, mock_output_dir, mock_lesson_plan_data):
        """Test that outputs are saved to the correct files."""
        from src.config.config import Config
        
        # Mock crew with tasks
        mock_crew = MagicMock()
        mock_output = MagicMock()
        mock_output.json_dict = mock_lesson_plan_data
        mock_output.raw = "Test content"
        
        mock_task = MagicMock()
        mock_task.output = mock_output
        mock_crew.tasks = [mock_task, mock_task, mock_task, mock_task]
        
        save_content_outputs("Test Topic", mock_crew)
        
        output_dir = Config.get_output_path("Test Topic")
        assert (output_dir / 'lesson_plan.md').exists()
        assert (output_dir / 'quiz_answer_key.md').exists()
        assert (output_dir / 'complete_content.md').exists()
    
    def test_save_content_outputs_handles_no_json_dict(self, mock_output_dir, capsys):
        """Test handling tasks without json_dict."""
        from src.config.config import Config
        
        mock_crew = MagicMock()
        mock_output = MagicMock()
        mock_output.raw = "Plain text output"
        del mock_output.json_dict  # Remove json_dict attribute
        
        mock_task = MagicMock()
        mock_task.output = mock_output
        mock_crew.tasks = [mock_task]
        
        save_content_outputs("Test", mock_crew)
        
        output_dir = Config.get_output_path("Test")
        assert (output_dir / 'lesson_plan.md').exists()
    
    def test_save_content_outputs_empty_tasks(self, mock_output_dir):
        """Test with no tasks."""
        from src.config.config import Config
        
        mock_crew = MagicMock()
        mock_crew.tasks = []
        
        save_content_outputs("Empty", mock_crew)
        
        # Should create complete_content.md even with no tasks
        output_dir = Config.get_output_path("Empty")
        assert (output_dir / 'complete_content.md').exists()
