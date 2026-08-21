"""
Slides Agent Schemas
====================
Data structures for presentation outputs.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class SlideContent(BaseModel):
    """Schema for a single slide."""
    
    slide_number: int = Field(
        description="Sequential slide number",
        ge=1
    )
    title: str = Field(
        description="Slide title/heading"
    )
    content_type: str = Field(
        description="Type of content: text, bullet_points, code, diagram, example"
    )
    content: str = Field(
        description="Main content of the slide (Markdown formatted)"
    )
    speaker_notes: Optional[str] = Field(
        default=None,
        description="Optional notes for the instructor/learner"
    )


class PresentationSlides(BaseModel):
    """Schema for complete presentation output from Slides Agent."""
    
    topic: str = Field(
        description="The topic these slides cover"
    )
    total_slides: int = Field(
        description="Total number of slides",
        ge=10,
        le=20
    )
    slides: List[SlideContent] = Field(
        description="Individual slides in order"
    )
    design_notes: str = Field(
        description="Notes about the presentation structure and flow"
    )

    @model_validator(mode="after")
    def validate_slide_consistency(self) -> "PresentationSlides":
        """Ensure slide count and numbering agree with the slide collection."""
        if len(self.slides) != self.total_slides:
            raise ValueError("total_slides must equal the number of slides")

        expected_numbers = list(range(1, len(self.slides) + 1))
        actual_numbers = [slide.slide_number for slide in self.slides]
        if actual_numbers != expected_numbers:
            raise ValueError("slide numbers must be contiguous and start at 1")
        return self
