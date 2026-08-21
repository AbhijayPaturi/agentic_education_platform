"""
Principal Agent Schemas
=======================
Data structures for curriculum planning outputs.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class TopicProposal(BaseModel):
    """Schema for a single topic in the curriculum."""
    
    topic_name: str = Field(
        description="Clear, concise name for the topic"
    )
    rationale: str = Field(
        description="2-3 sentence explanation of why this topic is important"
    )
    days_allocated: int = Field(
        description="Number of days to spend on this topic",
        ge=1,
        le=10
    )
    prerequisites: Optional[str] = Field(
        default=None,
        description="Prerequisites for this topic, if any"
    )
    order: int = Field(
        description="Sequential order in the curriculum (1-based)"
    )


class CurriculumProposal(BaseModel):
    """Schema for the complete curriculum output from Principal Agent."""
    
    user_name: str = Field(
        description="Name of the learner"
    )
    career_goal: str = Field(
        description="The learner's stated career goal"
    )
    curriculum_overview: str = Field(
        description="High-level overview of the learning path (2-3 paragraphs)"
    )
    topics: List[TopicProposal] = Field(
        description="Ordered list of 4-6 topics to cover",
        min_length=4,
        max_length=6
    )
    total_duration_days: int = Field(
        description="Total duration of the curriculum in days",
        ge=20,
        le=35
    )
    success_criteria: List[str] = Field(
        description="3-5 measurable outcomes the learner should achieve"
    )

    @model_validator(mode="after")
    def validate_curriculum_consistency(self) -> "CurriculumProposal":
        """Ensure topic order and duration agree with curriculum metadata."""
        expected_order = list(range(1, len(self.topics) + 1))
        actual_order = [topic.order for topic in self.topics]
        if actual_order != expected_order:
            raise ValueError("topic order must be contiguous and start at 1")

        allocated_days = sum(topic.days_allocated for topic in self.topics)
        if allocated_days != self.total_duration_days:
            raise ValueError(
                "total_duration_days must equal the sum of topic days_allocated"
            )
        return self
