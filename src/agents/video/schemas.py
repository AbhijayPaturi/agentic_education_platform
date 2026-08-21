"""
Video Agent Schemas
===================
Data structures for video resource outputs.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List


class VideoResource(BaseModel):
    """Schema for a single video resource suggestion."""
    
    title: str = Field(
        description="Descriptive title for the video"
    )
    description: str = Field(
        description="What the video covers and why it's relevant"
    )
    estimated_duration: str = Field(
        description="Estimated video length (e.g., '15 minutes', '1 hour')"
    )
    difficulty_level: str = Field(
        description="Beginner, Intermediate, or Advanced"
    )
    rationale: str = Field(
        description="Explanation of why this video was selected"
    )
    key_topics_covered: List[str] = Field(
        description="Main topics/concepts covered in the video"
    )
    suggested_viewing_order: int = Field(
        description="When in the learning sequence to watch this",
        ge=1
    )
    recommended_channel: str = Field(
        description="A reputable YouTube channel/creator likely to host this content "
                    "(e.g., 'freeCodeCamp', '3Blue1Brown', 'Fireship')"
    )
    search_query: str = Field(
        description="A concise, copy-paste YouTube search query to find this video"
    )
    hypothetical_url: str = Field(
        description="A working YouTube SEARCH URL that runs the search_query, e.g. "
                    "https://www.youtube.com/results?search_query=transformer+architecture+explained"
    )


class VideoResources(BaseModel):
    """Schema for video resource URLs from Video Agent."""
    
    topic: str = Field(
        description="The topic these videos support"
    )
    videos: List[VideoResource] = Field(
        description="5-8 video URL suggestions",
        min_length=5,
        max_length=8
    )
    viewing_guide: str = Field(
        description="Guidance on how to best use these video resources"
    )

    @model_validator(mode="after")
    def validate_viewing_order(self) -> "VideoResources":
        """Ensure resources are presented in a complete, unambiguous sequence."""
        expected_order = list(range(1, len(self.videos) + 1))
        actual_order = [video.suggested_viewing_order for video in self.videos]
        if actual_order != expected_order:
            raise ValueError("suggested viewing order must be contiguous and start at 1")
        return self
