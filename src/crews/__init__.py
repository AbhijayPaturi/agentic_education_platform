"""
Crews Module
============
Defines how agents and tasks come together to form teams.
"""

from .curriculum_crew import CurriculumCrew
from .content_generation_crew import ContentGenerationCrew

__all__ = ['CurriculumCrew', 'ContentGenerationCrew']
