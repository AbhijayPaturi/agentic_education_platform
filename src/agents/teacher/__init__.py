"""
Teacher Agent Module
====================
Detailed lesson planning and pedagogical design.
"""

from .agent import create_teacher_agent, create_lesson_planning_task
from .schemas import LessonPlan, LessonDetail, LearningObjective

__all__ = [
    'create_teacher_agent',
    'create_lesson_planning_task',
    'LessonPlan',
    'LessonDetail',
    'LearningObjective'
]
