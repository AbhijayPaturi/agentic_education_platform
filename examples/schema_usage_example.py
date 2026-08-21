"""Build and format a validated lesson plan without making an API call.

Run from the project root:

    python -m examples.schema_usage_example

This example demonstrates the contract used between agents: Pydantic validates
structured data, then the same object can be serialized for applications or
formatted as student-friendly Markdown.
"""

import json

from src.agents.teacher.schemas import LearningObjective, LessonDetail, LessonPlan
from src.utils.output_utils import format_lesson_plan


def build_lesson_plan() -> LessonPlan:
    """Create a small but complete lesson-plan artifact."""
    objectives = [
        LearningObjective(
            objective="Explain how tabular data moves through an analysis workflow",
            blooms_level="Understand",
        ),
        LearningObjective(
            objective="Build a reproducible pandas data-cleaning pipeline",
            blooms_level="Apply",
        ),
        LearningObjective(
            objective="Evaluate data quality before communicating results",
            blooms_level="Evaluate",
        ),
    ]
    lessons = [
        LessonDetail(
            lesson_number=number,
            title=title,
            learning_objective=objective,
            key_concepts=concepts,
            duration_minutes=45,
            teaching_approach="Short concept review followed by a notebook exercise",
            resources_needed=["Python 3.10+", "pandas", "JupyterLab"],
        )
        for number, title, objective, concepts in [
            (
                1,
                "Inspect the Dataset",
                "Profile schema and missingness",
                ["schema", "nulls", "types"],
            ),
            (
                2,
                "Clean Reproducibly",
                "Create a repeatable cleaning pipeline",
                ["functions", "validation", "logging"],
            ),
            (
                3,
                "Test Data Quality",
                "Write checks for analytical assumptions",
                ["assertions", "ranges", "uniqueness"],
            ),
            (
                4,
                "Communicate Findings",
                "Produce a concise quality report",
                ["metrics", "visuals", "limitations"],
            ),
        ]
    ]
    return LessonPlan(
        topic="Production-Ready Data Cleaning with pandas",
        overview=(
            "Learn a practical workflow for turning raw tabular data into a "
            "validated, reproducible analytical dataset."
        ),
        learning_objectives=objectives,
        lessons=lessons,
        assessment_strategy="Submit a tested cleaning pipeline and a one-page quality report.",
        estimated_total_time=sum(lesson.duration_minutes for lesson in lessons),
    )


def main() -> None:
    """Print both machine-readable and student-readable representations."""
    lesson_plan = build_lesson_plan()
    data = lesson_plan.model_dump()

    print("=== JSON ===")
    print(json.dumps(data, indent=2))
    print("\n=== MARKDOWN ===")
    print(format_lesson_plan(data))


if __name__ == "__main__":
    main()
