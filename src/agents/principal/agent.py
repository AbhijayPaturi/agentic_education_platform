"""Principal agent for curriculum design and strategic planning."""

from crewai import Agent, Task
from src.config.config import Config
from .schemas import CurriculumProposal


def create_principal_agent() -> Agent:
    """Create curriculum designer agent.
    
    Returns:
        Agent configured for strategic curriculum planning
    """
    return Agent(
        role='Academic Principal & Curriculum Designer',
        
        goal=(
            'Leverage your comprehensive internal knowledge of career development, '
            'skill requirements, and educational theory to analyze a user\'s career '
            'goals and design a complete, month-long list of learning topics. '
            'Create a logical progression that builds from foundational to advanced concepts.'
        ),
        
        backstory=(
            'You are a distinguished academic advisor with 30+ years of experience '
            'across multiple domains including technology, business, science, and humanities. '
            'You have guided thousands of professionals through career transitions and skill '
            'development. Your expertise lies in:\n'
            '- Breaking down complex career goals into learnable skills\n'
            '- Designing curriculum that respects learning dependencies\n'
            '- Balancing breadth and depth for time-constrained learners\n'
            '- Understanding industry trends and skill market demands\n'
            'You pride yourself on creating structured, achievable learning paths '
            'that respect the learner\'s time while maximizing educational impact.'
        ),
        
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=Config.DEFAULT_MODEL
    )


def create_topic_identification_task(
    principal_agent: Agent,
    user_name: str,
    career_goal: str
) -> Task:
    """Create task for identifying learning topics based on career goals.
    
    Args:
        principal_agent: Configured principal agent instance
        user_name: Learner's name for personalization
        career_goal: Career objective to analyze
        
    Returns:
        Task that outputs CurriculumProposal schema
    """
    return Task(
        description=(
            f"Analyze the career goal provided by {user_name}: '{career_goal}'\n\n"
            "Based on this goal, design a comprehensive month-long learning curriculum. "
            "Your output should:\n"
            "1. Identify 4-6 key topics the learner needs to master\n"
            "2. Order topics logically (foundational -> advanced)\n"
            "3. For each topic, provide:\n"
            "   - Topic name (clear and specific)\n"
            "   - Brief rationale (why this topic is essential)\n"
            "   - Estimated time allocation (in days)\n"
            "   - Prerequisites (if any)\n\n"
            "Consider:\n"
            "- The learner has approximately 30 days\n"
            "- Balance breadth (variety) with depth (mastery)\n"
            "- Include both technical skills and soft skills if relevant\n"
            "- Ensure topics build upon each other logically\n\n"
            "Format your output as a numbered list with clear topic names "
            "that can be easily extracted for processing."
        ),
        
        expected_output=(
            "A structured curriculum proposal following the CurriculumProposal schema with:\n"
            "- user_name: The learner's name\n"
            "- career_goal: Their stated goal\n"
            "- curriculum_overview: 2-3 paragraph overview\n"
            "- topics: List of 4-6 TopicProposal objects, each with:\n"
            "  * topic_name: Clear, concise name\n"
            "  * rationale: 2-3 sentence explanation\n"
            "  * days_allocated: 1-10 days\n"
            "  * prerequisites: Optional string\n"
            "  * order: Sequential position (1-based)\n"
            "- total_duration_days: 20-35 days total\n"
            "- success_criteria: 3-5 measurable outcomes\n\n"
            "The structured output enables automatic validation and processing."
        ),
        
        agent=principal_agent,
        output_json=CurriculumProposal,
        output_file=str(Config.OUTPUT_DIR / 'curriculum_proposal.md')
    )
