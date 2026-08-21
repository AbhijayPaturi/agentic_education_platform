"""Teacher agent for detailed lesson planning."""

from crewai import Agent, Task
from src.config.config import Config
from src.utils.text_utils import sanitize_filename
from .schemas import LessonPlan


def create_teacher_agent() -> Agent:
    """Create lesson planning agent.
    
    Returns:
        Agent configured for breaking down topics into structured lessons
    """
    return Agent(
        role='Master Educator & Lesson Planner',
        
        goal=(
            'For a given topic, create a detailed lesson-by-lesson plan using your '
            'internal teaching expertise and subject knowledge. Each lesson should have:\n'
            '- A clear, measurable learning objective\n'
            '- Estimated duration\n'
            '- Key concepts to be covered\n'
            '- Suggested activities or examples\n'
            'Ensure lessons build upon each other logically.'
        ),
        
        backstory=(
            'You are a master educator who has taught thousands of students across '
            'diverse subjects and skill levels. Your teaching philosophy is rooted in '
            'constructivist learning theory - building new knowledge on existing foundations. '
            'You excel at:\n'
            '- Breaking complex topics into digestible lessons\n'
            '- Identifying common misconceptions and addressing them proactively\n'
            '- Creating engaging lesson structures that maintain student interest\n'
            '- Balancing theoretical understanding with practical application\n'
            '- Adapting content for different learning styles\n'
            'Your lesson plans are known for their clarity, logical flow, and effectiveness.'
        ),
        
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=Config.DEFAULT_MODEL
    )


def create_lesson_planning_task(
    teacher_agent: Agent,
    topic: str
) -> Task:
    """Create task for generating detailed lesson plan.
    
    Args:
        teacher_agent: Configured teacher agent instance
        topic: Topic to break down into lessons
        
    Returns:
        Task that outputs LessonPlan schema
    """
    output_file = Config.OUTPUT_DIR / sanitize_filename(topic) / 'lesson_plan.md'
    
    return Task(
        description=(
            f"Create a detailed lesson plan for the topic: '{topic}'\n\n"
            "Your output must follow the LessonPlan schema structure:\n\n"
            "1. **topic**: The topic name (string)\n"
            "2. **overview**: 2-3 paragraph description of what this topic covers\n"
            "3. **learning_objectives**: List of 3-5 LearningObjective objects, each with:\n"
            "   - objective: Measurable statement starting with action verb\n"
            "   - blooms_level: One of [Remember, Understand, Apply, Analyze, Evaluate, Create]\n"
            "4. **lessons**: List of 4-6 LessonDetail objects, each with:\n"
            "   - lesson_number: Sequential number (starting at 1)\n"
            "   - title: Clear, descriptive lesson title\n"
            "   - learning_objective: Specific objective for this lesson\n"
            "   - key_concepts: List of 3-5 key concepts covered\n"
            "   - duration_minutes: Estimated time (15-120 minutes)\n"
            "   - teaching_approach: Recommended teaching method\n"
            "   - resources_needed: Optional list of materials/tools\n"
            "5. **assessment_strategy**: How learning will be validated (string)\n"
            "6. **estimated_total_time**: Total minutes for all lessons (integer)\n\n"
            "Ensure lessons:\n"
            "- Build progressively from simple to complex\n"
            "- Include a mix of theory and hands-on practice\n"
            "- Center on a concrete, portfolio-worthy project or deliverable\n"
            "- Reference MODERN, industry-standard tools, libraries, and workflows\n"
            "- Are appropriate for a motivated adult learner\n"
            "- Follow Bloom's Taxonomy for learning objectives\n"
            "- Meet all schema constraints (e.g., 4-6 lessons, 15-120 minutes each)"
        ),
        
        expected_output=(
            "A structured lesson plan following the LessonPlan schema. "
            "The schema ensures proper structure with validated data types, "
            "required fields, and constraints. This structured format enables:\n"
            "- Automatic validation of lesson plan completeness\n"
            "- Type-safe access to lesson components\n"
            "- Easy context passing to downstream agents\n"
            "- Both JSON (for processing) and Markdown (for humans) output formats"
        ),
        
        agent=teacher_agent,
        context=[],
        output_json=LessonPlan,
        output_file=str(output_file)
    )
