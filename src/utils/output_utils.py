"""Utilities for formatting and saving crew outputs."""

import json
from typing import Dict, Any


def print_banner(text: str, char: str = "=") -> None:
    """Print formatted banner for section headers.
    
    Args:
        text: Banner text to display
        char: Character to use for border
    """
    print(f"\n{char * 80}")
    print(f"{text:^80}")
    print(f"{char * 80}\n")


def print_section(title: str) -> None:
    """Print section header with divider.
    
    Args:
        title: Section title to display
    """
    print(f"\n{'─' * 80}")
    print(f"▶ {title}")
    print(f"{'─' * 80}\n")


def format_lesson_plan(data: Dict[str, Any]) -> str:
    """Convert LessonPlan schema to Markdown format.
    
    Args:
        data: Parsed lesson plan schema dict
        
    Returns:
        Formatted markdown string
    """
    lines = [f"# Lesson Plan: {data.get('topic', 'Unknown')}\n"]
    lines.append(f"## Overview\n{data.get('overview', '')}\n")
    lines.append("## Learning Objectives\n")
    for obj in data.get('learning_objectives', []):
        lines.append(f"- **{obj['objective']}** ({obj.get('blooms_level', 'N/A')})")
    lines.append("\n## Lessons\n")
    for lesson in data.get('lessons', []):
        lines.append(f"### Lesson {lesson['lesson_number']}: {lesson['title']}\n")
        lines.append(f"- **Objective**: {lesson['learning_objective']}")
        lines.append(f"- **Duration**: {lesson['duration_minutes']} minutes")
        lines.append(f"- **Key Concepts**: {', '.join(lesson['key_concepts'])}")
        lines.append(f"- **Teaching Approach**: {lesson['teaching_approach']}")
        if lesson.get('resources_needed'):
            lines.append(f"- **Resources**: {', '.join(lesson['resources_needed'])}")
        lines.append("")
    lines.append(f"## Assessment Strategy\n{data.get('assessment_strategy', '')}\n")
    lines.append(f"**Total Time**: {data.get('estimated_total_time', 0)} minutes")
    return '\n'.join(lines)


def format_slides(data: Dict[str, Any]) -> str:
    """Convert PresentationSlides schema to Markdown format.
    
    Args:
        data: Parsed presentation slides schema dict
        
    Returns:
        Formatted markdown string
    """
    lines = [f"# Presentation: {data.get('topic', 'Unknown')}\n"]
    lines.append(f"**Total Slides**: {data.get('total_slides', 0)}\n")
    for slide in data.get('slides', []):
        lines.append("---\n")
        lines.append(f"## {slide['title']}\n")
        lines.append(f"*Type: {slide.get('content_type', 'text')}*\n")
        lines.append(f"{slide['content']}\n")
        if slide.get('speaker_notes'):
            lines.append(f"> **Notes**: {slide['speaker_notes']}\n")
    lines.append(f"\n---\n\n## Design Notes\n{data.get('design_notes', '')}")
    return '\n'.join(lines)


def format_videos(data: Dict[str, Any]) -> str:
    """Convert VideoResources schema to Markdown format.
    
    Args:
        data: Parsed video resources schema dict
        
    Returns:
        Formatted markdown string
    """
    lines = [f"# Video Resources: {data.get('topic', 'Unknown')}\n"]
    for video in data.get('videos', []):
        lines.append(f"## {video['title']}\n")
        lines.append(f"- **Duration**: {video['estimated_duration']}")
        lines.append(f"- **Difficulty**: {video['difficulty_level']}")
        lines.append(f"- **Viewing Order**: {video['suggested_viewing_order']}")
        if video.get('recommended_channel'):
            lines.append(f"- **Recommended Channel**: {video['recommended_channel']}")
        if video.get('search_query'):
            lines.append(f"- **Search Query**: `{video['search_query']}`")
        url = video.get('hypothetical_url') or video.get('search_url', '')
        if url:
            lines.append(f"- **Find it**: [Search on YouTube]({url})")
        lines.append(f"- **Description**: {video['description']}")
        lines.append(f"- **Rationale**: {video['rationale']}")
        lines.append(f"- **Topics**: {', '.join(video['key_topics_covered'])}\n")
    lines.append(f"\n## Viewing Guide\n{data.get('viewing_guide', '')}")
    return '\n'.join(lines)


def format_quiz(data: Dict[str, Any]) -> str:
    """Convert Quiz schema to student-facing Markdown without answers.
    
    Args:
        data: Parsed quiz schema dict
        
    Returns:
        Formatted markdown string
    """
    lines = [f"# Quiz: {data.get('topic', 'Unknown')}\n"]
    lines.append(f"**Type**: {data.get('quiz_type', 'practice')}")
    lines.append(f"**Total Points**: {data.get('total_points', 0)}")
    lines.append(f"**Time Limit**: {data.get('time_limit_minutes', 0)} minutes")
    lines.append(f"**Passing Score**: {data.get('passing_score', 70)}%\n")
    lines.append("## Questions\n")
    for q in data.get('questions', []):
        lines.append(f"### Question {q['question_number']} ({q['difficulty']})\n")
        lines.append(f"**Type**: {q['question_type']}\n")
        lines.append(f"{q['question']}\n")
        if q.get('options'):
            for opt in q['options']:
                lines.append(f"- {opt}")
            lines.append("")
        lines.append(f"*Tests*: {q['learning_objective_tested']}\n")
        lines.append("---\n")
    lines.append(f"## Study Tips\n{data.get('study_tips', '')}")
    return '\n'.join(lines)


def format_quiz_answer_key(data: Dict[str, Any]) -> str:
    """Convert Quiz schema to a separate answer key with explanations."""
    lines = [f"# Answer Key: {data.get('topic', 'Unknown')}\n"]
    lines.append(
        "> Complete the quiz before opening this file. Use the explanations "
        "to review mistakes and identify topics to revisit.\n"
    )
    for question in data.get('questions', []):
        lines.append(f"## Question {question['question_number']}\n")
        lines.append(f"**Answer**: {question['correct_answer']}\n")
        lines.append(f"**Explanation**: {question['explanation']}\n")
        lines.append(f"**Learning Objective**: {question['learning_objective_tested']}\n")
    return '\n'.join(lines)


def save_content_outputs(topic: str, content_crew: Any) -> None:
    """Save generated educational content to structured files.

    Writes each task output as both validated JSON (when available) and
    human-readable Markdown, plus a consolidated ``complete_content.md`` backup.

    Args:
        topic: Topic name for directory organization
        content_crew: Completed ContentGenerationCrew with task outputs
    """
    from src.config.config import Config  # Local import avoids circular dependency.

    output_path = Config.get_output_path(topic)
    tasks = content_crew.tasks

    # (task_index, json_filename, markdown_filename, formatter, label)
    task_specs = [
        (0, 'lesson_plan.json', 'lesson_plan.md', format_lesson_plan, 'Lesson plan'),
        (1, 'slides.json', 'slides.md', format_slides, 'Slides'),
        (2, 'video_resources.json', 'video_resources.md', format_videos, 'Video resources'),
        (3, 'quiz.json', 'quiz.md', format_quiz, 'Quiz'),
    ]

    for index, json_name, md_name, formatter, label in task_specs:
        if index >= len(tasks):
            continue
        output = getattr(tasks[index], 'output', None)
        if not output:
            continue

        if hasattr(output, 'json_dict') and output.json_dict:
            json_data = output.json_dict
            markdown_content = formatter(json_data)
            with open(output_path / json_name, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            if index == 3:
                with open(output_path / 'quiz_answer_key.md', 'w', encoding='utf-8') as f:
                    f.write(format_quiz_answer_key(json_data))
        else:
            markdown_content = str(getattr(output, 'raw', output))

        with open(output_path / md_name, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"   ✓ {label} saved")

    # Save consolidated raw output as a backup.
    with open(output_path / 'complete_content.md', 'w', encoding='utf-8') as f:
        f.write(f"# Educational Content: {topic}\n\n")
        f.write("Generated by Agentic Educational System\n\n")
        f.write("---\n\n")
        for i, task in enumerate(tasks):
            output = getattr(task, 'output', None)
            if output:
                task_content = str(getattr(output, 'raw', output))
                f.write(f"\n\n## Task {i + 1} Output\n\n")
                f.write(task_content)
                f.write("\n\n---\n")

    print(f"   ✓ All content saved to: {output_path}")
