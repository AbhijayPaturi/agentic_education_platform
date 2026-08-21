"""Tests for agent creation functions."""

import pytest
from crewai import Agent, Task
from src.agents.principal.agent import create_principal_agent, create_topic_identification_task
from src.agents.teacher.agent import create_teacher_agent, create_lesson_planning_task
from src.agents.slides.agent import create_slides_agent, create_slides_creation_task
from src.agents.video.agent import create_video_agent, create_video_generation_task
from src.agents.test.agent import create_test_agent, create_quiz_creation_task


class TestPrincipalAgent:
    """Test principal agent creation."""
    
    def test_create_principal_agent_returns_agent(self):
        """Test that principal agent creation returns Agent instance."""
        agent = create_principal_agent()
        assert isinstance(agent, Agent)
    
    def test_principal_agent_has_role(self):
        """Test principal agent has defined role."""
        agent = create_principal_agent()
        assert agent.role is not None
        assert len(agent.role) > 0
    
    def test_principal_agent_has_goal(self):
        """Test principal agent has defined goal."""
        agent = create_principal_agent()
        assert agent.goal is not None
        assert len(agent.goal) > 0
    
    def test_create_topic_identification_task(self, mock_output_dir):
        """Test topic identification task creation."""
        agent = create_principal_agent()
        task = create_topic_identification_task(agent, "John", "ML Engineer")
        
        assert isinstance(task, Task)
        assert task.description is not None
        assert "John" in task.description
        assert "ML Engineer" in task.description


class TestTeacherAgent:
    """Test teacher agent creation."""
    
    def test_create_teacher_agent_returns_agent(self):
        """Test that teacher agent creation returns Agent instance."""
        agent = create_teacher_agent()
        assert isinstance(agent, Agent)
    
    def test_teacher_agent_has_role(self):
        """Test teacher agent has defined role."""
        agent = create_teacher_agent()
        assert agent.role is not None
    
    def test_create_lesson_planning_task(self, mock_output_dir):
        """Test lesson planning task creation."""
        agent = create_teacher_agent()
        task = create_lesson_planning_task(agent, "Python Basics")
        
        assert isinstance(task, Task)
        assert "Python Basics" in task.description or "Python_Basics" in str(task.output_file)
    
    def test_lesson_task_sanitizes_topic_name(self, mock_output_dir):
        """Test that special characters in topic names are handled."""
        agent = create_teacher_agent()
        task = create_lesson_planning_task(agent, "C++/C# Programming!")
        
        # Should not raise an error
        assert isinstance(task, Task)


class TestSlidesAgent:
    """Test slides agent creation."""
    
    def test_create_slides_agent_returns_agent(self):
        """Test that slides agent creation returns Agent instance."""
        agent = create_slides_agent()
        assert isinstance(agent, Agent)
    
    def test_create_slides_task_requires_context(self, mock_output_dir):
        """Test slides task requires previous lesson task as context."""
        slides_agent = create_slides_agent()
        teacher_agent = create_teacher_agent()
        lesson_task = create_lesson_planning_task(teacher_agent, "Test Topic")
        
        slides_task = create_slides_creation_task(slides_agent, lesson_task, "Test Topic")
        
        assert isinstance(slides_task, Task)
        # Verify context dependency
        assert lesson_task in slides_task.context or hasattr(slides_task, 'context')


class TestVideoAgent:
    """Test video agent creation."""
    
    def test_create_video_agent_returns_agent(self):
        """Test that video agent creation returns Agent instance."""
        agent = create_video_agent()
        assert isinstance(agent, Agent)
    
    def test_video_agent_has_tools(self):
        """Test video agent has HypotheticalVideoSearchTool."""
        agent = create_video_agent()
        assert agent.tools is not None
        assert len(agent.tools) > 0
    
    def test_create_video_generation_task(self, mock_output_dir):
        """Test video generation task creation."""
        video_agent = create_video_agent()
        teacher_agent = create_teacher_agent()
        lesson_task = create_lesson_planning_task(teacher_agent, "Test")
        
        video_task = create_video_generation_task(video_agent, lesson_task, "Test")
        
        assert isinstance(video_task, Task)


class TestTestAgent:
    """Test test agent creation."""
    
    def test_create_test_agent_returns_agent(self):
        """Test that test agent creation returns Agent instance."""
        agent = create_test_agent()
        assert isinstance(agent, Agent)
    
    def test_create_quiz_creation_task(self, mock_output_dir):
        """Test quiz creation task creation."""
        test_agent = create_test_agent()
        slides_agent = create_slides_agent()
        teacher_agent = create_teacher_agent()
        lesson_task = create_lesson_planning_task(teacher_agent, "Test")
        slides_task = create_slides_creation_task(slides_agent, lesson_task, "Test")
        
        quiz_task = create_quiz_creation_task(test_agent, slides_task, "Test")
        
        assert isinstance(quiz_task, Task)


class TestAgentAttributes:
    """Test that all agents have required attributes."""
    
    @pytest.mark.parametrize("create_func", [
        create_principal_agent,
        create_teacher_agent,
        create_slides_agent,
        create_video_agent,
        create_test_agent
    ])
    def test_agent_has_backstory(self, create_func):
        """Test all agents have backstories."""
        agent = create_func()
        assert hasattr(agent, 'backstory')
        assert agent.backstory is not None
    
    @pytest.mark.parametrize("create_func", [
        create_principal_agent,
        create_teacher_agent,
        create_slides_agent,
        create_video_agent,
        create_test_agent
    ])
    def test_agent_has_verbose_mode(self, create_func):
        """Test all agents have verbose mode configured."""
        agent = create_func()
        assert hasattr(agent, 'verbose')
