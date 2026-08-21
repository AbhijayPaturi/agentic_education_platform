"""ContentGenerationCrew orchestrates tactical content creation at Level 2."""

from typing import Any, Dict, Optional
from crewai import Crew, Process
from src.config.config import Config
from src.agents.teacher import create_teacher_agent, create_lesson_planning_task
from src.agents.slides import create_slides_agent, create_slides_creation_task
from src.agents.video import create_video_agent, create_video_generation_task
from src.agents.test import create_test_agent, create_quiz_creation_task


class ContentGenerationCrew:
    """Tactical crew that generates complete educational content for a single topic."""
    
    def __init__(self, topic: str) -> None:
        """Initialize content generation crew.
        
        Args:
            topic: Specific topic to develop content for
        """
        self.topic = topic
        
        self.teacher = create_teacher_agent()
        self.slides = create_slides_agent()
        self.video = create_video_agent()
        self.test = create_test_agent()
        
        # Task chain: lesson -> slides -> video, quiz
        self.lesson_task = create_lesson_planning_task(self.teacher, topic)
        self.slides_task = create_slides_creation_task(self.slides, self.lesson_task, topic)
        self.video_task = create_video_generation_task(self.video, self.lesson_task, topic)
        self.quiz_task = create_quiz_creation_task(self.test, self.slides_task, topic)
        
        self.crew = Crew(
            agents=[self.teacher, self.slides, self.video, self.test],
            tasks=[self.lesson_task, self.slides_task, self.video_task, self.quiz_task],
            process=Process.sequential,
            verbose=Config.VERBOSE
        )
    
    def kickoff(self) -> Any:
        """Execute content generation process.
        
        Returns:
            Result from final quiz creation task
        """
        return self.crew.kickoff(inputs={'topic': self.topic})
    
    def get_all_outputs(self) -> Dict[str, Optional[Any]]:
        """Retrieve all task outputs after crew execution.
        
        Returns:
            Dictionary mapping task names to their outputs
        """
        return {
            'lesson_plan': self.lesson_task.output if hasattr(self.lesson_task, 'output') else None,
            'slides': self.slides_task.output if hasattr(self.slides_task, 'output') else None,
            'videos': self.video_task.output if hasattr(self.video_task, 'output') else None,
            'quiz': self.quiz_task.output if hasattr(self.quiz_task, 'output') else None
        }
