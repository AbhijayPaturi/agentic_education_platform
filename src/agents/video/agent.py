"""Video agent for educational resource curation."""

from crewai import Agent, Task
from src.config.config import Config
from src.tools.video_generation_tool import HypotheticalVideoSearchTool
from src.utils.text_utils import sanitize_filename
from .schemas import VideoResources


def create_video_agent() -> Agent:
    """Create video curation agent.
    
    Returns:
        Agent configured for suggesting relevant educational videos
    """
    return Agent(
        role='Digital Content Curator & Video Resource Specialist',
        
        goal=(
            'For each lesson, identify and suggest 3-5 relevant educational videos '
            'that would enhance student understanding. Generate plausible video titles, '
            'hypothetical URLs, and descriptions based on your knowledge of educational '
            'content available online. Focus on videos that:\n'
            '- Complement the lesson objectives\n'
            '- Offer different teaching perspectives or approaches\n'
            '- Vary in depth (overview to detailed)\n'
            '- Come from reputable educational sources'
        ),
        
        backstory=(
            'You are a digital learning specialist who has curated educational video '
            'content for major online learning platforms. You have an intuitive sense '
            'for what makes an effective educational video and understand the landscape '
            'of online educational content. Your expertise includes:\n'
            '- Identifying high-quality educational video content\n'
            '- Matching video resources to learning objectives\n'
            '- Understanding different teaching styles in video format\n'
            '- Predicting relevant video titles and content based on topic\n'
            'You understand that video resources provide alternative explanations and '
            'visual demonstrations that can significantly enhance learning, especially '
            'for complex or abstract concepts.'
        ),
        
        verbose=Config.VERBOSE,
        allow_delegation=False,
        tools=[HypotheticalVideoSearchTool],
        llm=Config.DEFAULT_MODEL
    )


def create_video_generation_task(
    video_agent: Agent,
    lesson_planning_task: Task,
    topic: str
) -> Task:
    """Create task for suggesting video resources.
    
    Args:
        video_agent: Configured video agent instance with search tool
        lesson_planning_task: Previous task providing lesson plan context
        topic: Topic for video suggestions
        
    Returns:
        Task that outputs VideoResources schema
    """
    output_file = Config.OUTPUT_DIR / sanitize_filename(topic) / 'video_resources.md'
    
    return Task(
        description=(
            f"Suggest relevant educational YouTube videos for the topic: '{topic}'\n\n"
            "Your output must follow the VideoResources schema structure:\n\n"
            "1. **topic**: The topic name (string)\n"
            "2. **videos**: List of 5-8 VideoResource objects, each with:\n"
            "   - title: Descriptive title for the video\n"
            "   - description: What the video covers and why it's relevant\n"
            "   - estimated_duration: Video length (e.g., '15 minutes', '1 hour')\n"
            "   - difficulty_level: One of [Beginner, Intermediate, Advanced]\n"
            "   - key_topics_covered: List of main topics/concepts\n"
            "   - suggested_viewing_order: When to watch (1-8)\n"
            "   - recommended_channel: A reputable creator (e.g., freeCodeCamp,\n"
            "     3Blue1Brown, StatQuest, Fireship) that fits the subject\n"
            "   - search_query: A concise, copy-paste YouTube search query\n"
            "   - hypothetical_url: A WORKING YouTube search URL of the form\n"
            "     https://www.youtube.com/results?search_query=<url-encoded-query>\n"
            "3. **viewing_guide**: Guidance on how to best use these resources\n\n"
            "Based on the lesson plan context (LessonPlan schema), use your "
            "YouTube Resource Finder tool to suggest videos that:\n"
            "- Cover key concepts from the lesson plan\n"
            "- Reflect MODERN, up-to-date tools and best practices\n"
            "- Offer different teaching perspectives\n"
            "- Vary in depth (overview, detailed deep-dives)\n"
            "- Progress logically (Beginner → Intermediate → Advanced)\n"
            "- Come from reputable educational channels\n\n"
            "IMPORTANT: Never invent fake /watch?v=... links (they lead to dead\n"
            "pages). Always provide a working search URL so learners reach live\n"
            "results, and explain in viewing_guide how to pick the best result."
        ),

        expected_output=(
            "A structured video resource guide following the VideoResources schema. "
            "The schema provides:\n"
            "- a working YouTube SEARCH URL for each suggestion (leads to live results)\n"
            "- a reputable recommended channel and copy-paste search query\n"
            "- Detailed metadata for each video suggestion\n"
            "- Difficulty progression tracking\n"
            "- Suggested viewing order for optimal learning\n"
            "- Comprehensive viewing guide\n"
            "- Rationale for why this video over others\n\n"
            "This structure helps learners find and use real video resources effectively."
        ),

        agent=video_agent,
        context=[lesson_planning_task],
        output_json=VideoResources,
        output_file=str(output_file)
    )
