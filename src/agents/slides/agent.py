"""Slides agent for presentation design."""

from crewai import Agent, Task
from src.config.config import Config
from src.utils.text_utils import sanitize_filename
from .schemas import PresentationSlides


def create_slides_agent() -> Agent:
    """Create presentation design agent.
    
    Returns:
        Agent configured for transforming lessons into slide decks
    """
    return Agent(
        role='Educational Content Designer & Presentation Specialist',
        
        goal=(
            'Transform lesson plans into clear, concise, and engaging presentation '
            'slides in Markdown format. Each slide should:\n'
            '- Focus on one key concept or idea\n'
            '- Use clear headings and bullet points\n'
            '- Include examples or analogies where helpful\n'
            '- Follow best practices for educational presentations\n'
            'Aim for 8-12 slides per lesson, structured for optimal learning.'
        ),
        
        backstory=(
            'You are a skilled instructional designer who specializes in creating '
            'compelling educational presentations. You understand the psychology of '
            'visual learning and information retention. Your expertise includes:\n'
            '- Applying cognitive load theory to slide design\n'
            '- Creating clear visual hierarchies\n'
            '- Balancing information density with comprehension\n'
            '- Using analogies and examples to reinforce concepts\n'
            '- Structuring content for maximum engagement\n'
            'Your slides are praised for being informative yet uncluttered, engaging '
            'yet professional. You know that great slides support learning rather than '
            'replace the teaching narrative.'
        ),
        
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=Config.DEFAULT_MODEL
    )


def create_slides_creation_task(
    slides_agent: Agent,
    lesson_planning_task: Task,
    topic: str
) -> Task:
    """Create task for generating presentation slides.
    
    Args:
        slides_agent: Configured slides agent instance
        lesson_planning_task: Previous task providing lesson plan context
        topic: Topic for slide generation
        
    Returns:
        Task that outputs PresentationSlides schema
    """
    output_file = Config.OUTPUT_DIR / sanitize_filename(topic) / 'slides.md'
    
    return Task(
        description=(
            f"Create presentation slides for the topic: '{topic}'\n\n"
            "Your output must follow the PresentationSlides schema structure:\n\n"
            "1. **topic**: The topic name (string)\n"
            "2. **total_slides**: Total number of slides (10-20)\n"
            "3. **slides**: List of SlideContent objects (10-20 slides), each with:\n"
            "   - slide_number: Sequential number (starting at 1)\n"
            "   - title: Slide title/heading\n"
            "   - content_type: One of [text, bullet_points, code, diagram, example]\n"
            "   - content: Main content in Markdown format (descriptive and detailed)\n"
            "   - speaker_notes: Optional notes for instructor/learner\n"
            "4. **design_notes**: Notes about presentation structure and flow\n\n"
            "Based on the lesson plan context (LessonPlan schema), create slides that:\n"
            "- Cover all learning objectives from the lesson plan\n"
            "- Present key concepts from each lesson\n"
            "- Include concrete, runnable code snippets and real-world examples\n"
            "- Reference MODERN tools, libraries, and current best practices\n"
            "- Use descriptive, text-heavy content suitable for self-paced learning\n"
            "- Follow slide design principles (one concept per slide, clear headings)\n"
            "- Are suitable for conversion to Marp, reveal.js, or similar formats\n\n"
            "Ensure all slides meet schema constraints and provide rich, educational content."
        ),
        
        expected_output=(
            "A structured presentation following the PresentationSlides schema. "
            "The schema provides:\n"
            "- Structured slide-by-slide content with metadata\n"
            "- Content type classification for each slide\n"
            "- Optional speaker notes for additional context\n"
            "- Design notes for overall presentation flow\n"
            "This enables both programmatic processing and human-readable output."
        ),
        
        agent=slides_agent,
        context=[lesson_planning_task],
        output_json=PresentationSlides,
        output_file=str(output_file)
    )
