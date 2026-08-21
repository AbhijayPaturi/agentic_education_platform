"""
Test Agent Schemas
==================
Data structures for quiz and assessment outputs.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class QuizQuestion(BaseModel):
    """Schema for a single quiz question."""
    
    question_number: int = Field(
        description="Sequential question number",
        ge=1
    )
    question_type: str = Field(
        description="Type: multiple_choice, true_false, short_answer, code_problem"
    )
    question: str = Field(
        description="The question text"
    )
    options: Optional[List[str]] = Field(
        default=None,
        description="Answer options for multiple choice questions"
    )
    correct_answer: str = Field(
        description="The correct answer"
    )
    explanation: str = Field(
        description="Explanation of why this is the correct answer"
    )
    difficulty: str = Field(
        description="Easy, Medium, or Hard"
    )
    learning_objective_tested: str = Field(
        description="Which learning objective this question assesses"
    )


class Quiz(BaseModel):
    """Schema for complete quiz output from Test Agent."""
    
    topic: str = Field(
        description="The topic being assessed"
    )
    quiz_type: str = Field(
        description="Type of assessment: formative, summative, practice"
    )
    total_points: int = Field(
        description="Total points available in the quiz",
        ge=10,
        le=100
    )
    time_limit_minutes: int = Field(
        description="Suggested time limit in minutes",
        ge=10,
        le=90
    )
    questions: List[QuizQuestion] = Field(
        description="10-15 questions",
        min_length=10,
        max_length=15
    )
    passing_score: int = Field(
        description="Percentage needed to pass",
        ge=60,
        le=80
    )
    study_tips: str = Field(
        description="Tips for preparing for this assessment"
    )

    @model_validator(mode="after")
    def validate_question_order(self) -> "Quiz":
        """Ensure questions have a complete, deterministic display order."""
        expected_numbers = list(range(1, len(self.questions) + 1))
        actual_numbers = [question.question_number for question in self.questions]
        if actual_numbers != expected_numbers:
            raise ValueError("question numbers must be contiguous and start at 1")
        return self
