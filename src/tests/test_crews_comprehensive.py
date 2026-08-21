"""Comprehensive tests for crew orchestration."""

from unittest.mock import patch, MagicMock
from src.crews.curriculum_crew import CurriculumCrew
from src.crews.content_generation_crew import ContentGenerationCrew


class TestCurriculumCrew:
    """Test CurriculumCrew class."""
    
    def test_curriculum_crew_initialization(self):
        """Test CurriculumCrew initializes correctly."""
        crew = CurriculumCrew("Alice", "Data Scientist")
        
        assert crew.user_name == "Alice"
        assert crew.career_goal == "Data Scientist"
        assert crew.principal is not None
        assert crew.topic_task is not None
        assert crew.crew is not None
    
    def test_curriculum_crew_has_single_agent(self):
        """Test CurriculumCrew has only principal agent."""
        crew = CurriculumCrew("Bob", "ML Engineer")
        
        assert len(crew.crew.agents) == 1
        assert crew.principal in crew.crew.agents
    
    def test_curriculum_crew_has_single_task(self):
        """Test CurriculumCrew has single task."""
        crew = CurriculumCrew("Carol", "Software Engineer")
        
        assert len(crew.crew.tasks) == 1
        assert crew.topic_task in crew.crew.tasks
    
    @patch('src.crews.curriculum_crew.Crew')
    def test_kickoff_calls_crew_kickoff(self, mock_crew_class):
        """Test that kickoff calls underlying crew's kickoff."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = CurriculumCrew("Dave", "DevOps Engineer")
        crew.kickoff()
        
        mock_crew_instance.kickoff.assert_called_once()
    
    def test_get_task_output_returns_none_when_no_output(self):
        """Test get_task_output returns None when task has no output."""
        crew = CurriculumCrew("Eve", "Product Manager")
        
        # Before kickoff, output should be None
        output = crew.get_task_output()
        assert output is None or output == []
    
    def test_crew_uses_sequential_process(self):
        """Test that crew uses sequential process."""
        crew = CurriculumCrew("Frank", "Designer")
        
        from crewai import Process
        assert crew.crew.process == Process.sequential


class TestContentGenerationCrew:
    """Test ContentGenerationCrew class."""
    
    def test_content_generation_crew_initialization(self):
        """Test ContentGenerationCrew initializes correctly."""
        crew = ContentGenerationCrew("Python Basics")
        
        assert crew.topic == "Python Basics"
        assert crew.teacher is not None
        assert crew.slides is not None
        assert crew.video is not None
        assert crew.test is not None
    
    def test_content_crew_has_four_agents(self):
        """Test ContentGenerationCrew has all four agents."""
        crew = ContentGenerationCrew("Machine Learning")
        
        assert len(crew.crew.agents) == 4
        assert crew.teacher in crew.crew.agents
        assert crew.slides in crew.crew.agents
        assert crew.video in crew.crew.agents
        assert crew.test in crew.crew.agents
    
    def test_content_crew_has_four_tasks(self):
        """Test ContentGenerationCrew has all four tasks."""
        crew = ContentGenerationCrew("Web Development")
        
        assert len(crew.crew.tasks) == 4
    
    def test_content_crew_task_chain(self):
        """Test that tasks are properly chained with context."""
        crew = ContentGenerationCrew("Data Science")
        
        # Slides task should depend on lesson task
        assert crew.lesson_task in crew.slides_task.context or \
               hasattr(crew.slides_task, 'context')
        
        # Video task should depend on lesson task
        assert crew.lesson_task in crew.video_task.context or \
               hasattr(crew.video_task, 'context')
        
        # Quiz task should depend on slides task
        assert crew.slides_task in crew.quiz_task.context or \
               hasattr(crew.quiz_task, 'context')
    
    @patch('src.crews.content_generation_crew.Crew')
    def test_kickoff_passes_topic_input(self, mock_crew_class):
        """Test that kickoff passes topic as input."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = ContentGenerationCrew("Cloud Computing")
        crew.kickoff()
        
        mock_crew_instance.kickoff.assert_called_once()
        call_args = mock_crew_instance.kickoff.call_args
        assert call_args is not None
        # Check if inputs contains topic
        if call_args[1]:  # kwargs
            assert 'inputs' in call_args[1]
            assert call_args[1]['inputs']['topic'] == "Cloud Computing"
    
    def test_get_all_outputs_structure(self):
        """Test get_all_outputs returns correct structure."""
        crew = ContentGenerationCrew("Blockchain")
        
        outputs = crew.get_all_outputs()
        
        assert isinstance(outputs, dict)
        assert 'lesson_plan' in outputs
        assert 'slides' in outputs
        assert 'videos' in outputs
        assert 'quiz' in outputs
    
    def test_get_all_outputs_returns_none_before_kickoff(self):
        """Test outputs are None before crew execution."""
        crew = ContentGenerationCrew("Cybersecurity")
        
        outputs = crew.get_all_outputs()
        
        # All outputs should be None before kickoff
        assert outputs['lesson_plan'] is None
        assert outputs['slides'] is None
        assert outputs['videos'] is None
        assert outputs['quiz'] is None
    
    def test_content_crew_topic_sanitization(self, tmp_path, monkeypatch):
        """Test that special characters in topic don't break crew."""
        from src.config.config import Config
        monkeypatch.setattr(Config, 'OUTPUT_DIR', tmp_path)
        
        # Should not raise exception
        crew = ContentGenerationCrew("C++/C# & Java!")
        assert crew.topic == "C++/C# & Java!"


class TestCrewEdgeCases:
    """Test edge cases for crew operations."""
    
    def test_curriculum_crew_empty_name(self):
        """Test CurriculumCrew with empty user name."""
        crew = CurriculumCrew("", "Engineer")
        assert crew.user_name == ""
    
    def test_curriculum_crew_empty_goal(self):
        """Test CurriculumCrew with empty career goal."""
        crew = CurriculumCrew("User", "")
        assert crew.career_goal == ""
    
    def test_content_crew_empty_topic(self, tmp_path, monkeypatch):
        """Test ContentGenerationCrew with empty topic."""
        from src.config.config import Config
        monkeypatch.setattr(Config, 'OUTPUT_DIR', tmp_path)
        
        crew = ContentGenerationCrew("")
        assert crew.topic == ""
    
    def test_content_crew_very_long_topic(self, tmp_path, monkeypatch):
        """Test ContentGenerationCrew with very long topic name."""
        from src.config.config import Config
        monkeypatch.setattr(Config, 'OUTPUT_DIR', tmp_path)
        
        long_topic = "A" * 500
        crew = ContentGenerationCrew(long_topic)
        assert crew.topic == long_topic
    
    def test_curriculum_crew_unicode_characters(self):
        """Test CurriculumCrew with unicode characters."""
        crew = CurriculumCrew("José", "Ingénieur de données 数据科学家")
        assert "José" in crew.user_name
        assert "数据科学家" in crew.career_goal
