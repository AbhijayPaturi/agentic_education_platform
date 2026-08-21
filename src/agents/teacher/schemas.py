"""
Teacher Agent Schemas
=====================
Data structures for lesson planning outputs.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class LearningObjective(BaseModel):
    """Schema for a single learning objective."""
    
    objective: str = Field(
        description="Measurable learning objective starting with an action verb"
    )
    blooms_level: str = Field(
        description="Bloom's Taxonomy level: Remember, Understand, Apply, Analyze, Evaluate, Create"
    )


class LessonDetail(BaseModel):
    """Schema for a single lesson within a lesson plan."""
    
    lesson_number: int = Field(
        description="Sequential lesson number",
        ge=1
    )
    title: str = Field(
        description="Clear, descriptive lesson title"
    )
    learning_objective: str = Field(
        description="Specific objective for this lesson"
    )
    key_concepts: List[str] = Field(
        description="3-5 key concepts covered in this lesson"
    )
    duration_minutes: int = Field(
        description="Estimated time to complete this lesson",
        ge=15,
        le=120
    )
    teaching_approach: str = Field(
        description="Recommended teaching method or activity"
    )
    resources_needed: Optional[List[str]] = Field(
        default=None,
        description="Materials, tools, or resources needed"
    )


class LessonPlan(BaseModel):
    """Schema for complete lesson plan output from Teacher Agent."""
    
    topic: str = Field(
        description="The topic this lesson plan covers"
    )
    overview: str = Field(
        description="2-3 paragraph overview of what this topic covers"
    )
    learning_objectives: List[LearningObjective] = Field(
        description="3-5 measurable learning objectives",
        min_length=3,
        max_length=5
    )
    lessons: List[LessonDetail] = Field(
        description="4-6 individual lessons",
        min_length=4,
        max_length=6
    )
    assessment_strategy: str = Field(
        description="How learning will be validated and assessed"
    )
    estimated_total_time: int = Field(
        description="Total estimated time in minutes for all lessons"
    )

    @model_validator(mode="after")
    def validate_lesson_consistency(self) -> "LessonPlan":
        """Ensure lesson numbering and duration metadata are internally consistent."""
        expected_numbers = list(range(1, len(self.lessons) + 1))
        actual_numbers = [lesson.lesson_number for lesson in self.lessons]
        if actual_numbers != expected_numbers:
            raise ValueError("lesson numbers must be contiguous and start at 1")

        lesson_minutes = sum(lesson.duration_minutes for lesson in self.lessons)
        if lesson_minutes != self.estimated_total_time:
            raise ValueError(
                "estimated_total_time must equal the sum of lesson durations"
            )
        return self
