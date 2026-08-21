"""CurriculumCrew orchestrates strategic curriculum design at Level 1."""

from typing import Any, Optional
from crewai import Crew, Process
from src.config.config import Config
from src.agents.principal import create_principal_agent, create_topic_identification_task


class CurriculumCrew:
    """Strategic crew that identifies learning topics based on career goals."""
    
    def __init__(self, user_name: str, career_goal: str) -> None:
        """Initialize curriculum planning crew.
        
        Args:
            user_name: Learner's name for personalization
            career_goal: Career objective to analyze
        """
        self.user_name = user_name
        self.career_goal = career_goal
        
        self.principal = create_principal_agent()
        self.topic_task = create_topic_identification_task(
            self.principal,
            user_name,
            career_goal
        )
        
        self.crew = Crew(
            agents=[self.principal],
            tasks=[self.topic_task],
            process=Process.sequential,
            verbose=Config.VERBOSE
        )
    
    def kickoff(self) -> Any:
        """Execute curriculum planning process.
        
        Returns:
            CurriculumProposal containing identified topics
        """
        return self.crew.kickoff()
    
    def get_task_output(self) -> Optional[Any]:
        """Retrieve task output after crew execution.
        
        Returns:
            Task output if available, None otherwise
        """
        if self.crew.tasks and self.crew.tasks[0].output:
            return self.crew.tasks[0].output
        return None
