"""Test agent for assessment design."""

from crewai import Agent, Task
from src.config.config import Config
from src.utils.text_utils import sanitize_filename
from .schemas import Quiz


def create_test_agent() -> Agent:
    """Create assessment design agent.
    
    Returns:
        Agent configured for creating educational quizzes
    """
    return Agent(
        role='Educational Assessment Specialist',
        
        goal=(
            'For each lesson, create a 5-question multiple-choice quiz that effectively '
            'assesses student understanding. Each question should:\n'
            '- Test a key concept from the lesson\n'
            '- Have one clearly correct answer\n'
            '- Include 3-4 plausible distractors (wrong answers)\n'
            '- Be unambiguous and clearly worded\n'
            'Include an answer key with brief explanations.'
        ),
        
        backstory=(
            'You are an experienced educational psychologist and assessment designer '
            'who has created thousands of test questions for various educational levels. '
            'You understand the science of assessment and measurement. Your expertise includes:\n'
            '- Applying Bloom\'s Taxonomy to test different cognitive levels\n'
            '- Writing clear, unambiguous questions\n'
            '- Creating plausible distractors that reveal common misconceptions\n'
            '- Avoiding common question-writing pitfalls (ambiguity, "all of the above", etc.)\n'
            '- Balancing question difficulty to accurately measure understanding\n'
            'Your assessments are known for fairly and accurately measuring student learning '
            'while providing educational value through well-crafted distractors that highlight '
            'important distinctions.'
        ),
        
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=Config.DEFAULT_MODEL
    )


def create_quiz_creation_task(
    test_agent: Agent,
    slides_creation_task: Task,
    topic: str
) -> Task:
    """Create task for generating assessment quiz.
    
    Args:
        test_agent: Configured test agent instance
        slides_creation_task: Previous task providing slides context
        topic: Topic to assess
        
    Returns:
        Task that outputs Quiz schema
    """
    output_file = Config.OUTPUT_DIR / sanitize_filename(topic) / 'quiz.md'
    
    return Task(
        description=(
            f"Create a comprehensive quiz for the topic: '{topic}'\n\n"
            "Your output must follow the Quiz schema structure:\n\n"
            "1. **topic**: The topic being assessed (string)\n"
            "2. **quiz_type**: One of [formative, summative, practice]\n"
            "3. **total_points**: Total points available (10-100)\n"
            "4. **time_limit_minutes**: Suggested time limit (10-90 minutes)\n"
            "5. **questions**: List of 10-15 QuizQuestion objects, each with:\n"
            "   - question_number: Sequential number (starting at 1)\n"
            "   - question_type: One of [multiple_choice, true_false, short_answer, code_problem]\n"
            "   - question: The question text (clear and unambiguous)\n"
            "   - options: List of choices (for multiple_choice only)\n"
            "   - correct_answer: The correct answer\n"
            "   - explanation: Why this is correct (2-3 sentences)\n"
            "   - difficulty: One of [Easy, Medium, Hard]\n"
            "   - learning_objective_tested: Which objective this assesses\n"
            "6. **passing_score**: Percentage needed to pass (60-80)\n"
            "7. **study_tips**: Preparation guidance (string)\n\n"
            "Based on the slides context (PresentationSlides schema), create questions that:\n"
            "- Test key concepts presented in the slides\n"
            "- Emphasize application and problem-solving over rote recall\n"
            "- Mix difficulty levels (30% Easy, 50% Medium, 20% Hard)\n"
            "- Include various question types\n"
            "- Align with learning objectives\n"
            "- Provide clear, helpful explanations\n"
            "- Avoid trick questions and \"all/none of the above\" options\n\n"
            "Ensure all questions meet schema constraints and assess understanding effectively."
        ),
        
        expected_output=(
            "A structured quiz following the Quiz schema. "
            "The schema provides:\n"
            "- Complete question metadata (type, difficulty, learning objectives)\n"
            "- Structured answer options and explanations\n"
            "- Quiz configuration (time limit, passing score, points)\n"
            "- Study tips for preparation\n"
            "This enables automated quiz administration, grading, and analytics."
        ),
        
        agent=test_agent,
        context=[slides_creation_task],
        output_json=Quiz,
        output_file=str(output_file)
    )
