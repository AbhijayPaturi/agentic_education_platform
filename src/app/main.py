"""Main application entry point for educational content generation system."""

import sys
import re
import os
import traceback
from pathlib import Path
from typing import List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config.config import Config  # noqa: E402
from src.crews import CurriculumCrew, ContentGenerationCrew  # noqa: E402
from src.utils.output_utils import (  # noqa: E402
    save_content_outputs,
    print_banner,
    print_section
)


def get_user_input() -> Tuple[str, str]:
    """Gather user input for personalized curriculum generation.
    
    Returns:
        Tuple of (user_name, career_goal)
    """
    print_banner("🎓 Welcome to the Agentic Educational System", "=")
    
    print("This intelligent system will create a personalized month-long learning")
    print("curriculum tailored to your career goals, complete with lessons, slides,")
    print("video suggestions, and quizzes.\n")
    
    # Get user name
    user_name = input("What's your name? ").strip()
    while not user_name:
        print("Please enter your name.")
        user_name = input("What's your name? ").strip()
    
    print(f"\nGreat to meet you, {user_name}! 👋\n")
    
    # Get career goal
    print("Please describe your career goal or the skills you want to develop.")
    print("Be as specific as possible for the best results.")
    print("\nExamples:")
    print("  • 'Transition from web development to machine learning engineering'")
    print("  • 'Become a data analyst with Python and SQL skills'")
    print("  • 'Learn cloud architecture on AWS for DevOps role'\n")
    
    career_goal = input("Your career goal: ").strip()
    while not career_goal or len(career_goal) < 10:
        print("Please provide a more detailed career goal (at least 10 characters).")
        career_goal = input("Your career goal: ").strip()
    
    return user_name, career_goal


def parse_topics_from_output(curriculum_crew: CurriculumCrew) -> List[str]:
    """Extract topic names from curriculum proposal.
    
    Args:
        curriculum_crew: Completed CurriculumCrew instance
        
    Returns:
        List of topic names in order
    """
    topics: List[str] = []
    
    task_output = curriculum_crew.get_task_output()
    if not task_output:
        return topics
    
    # Try structured output first
    if hasattr(task_output, 'json_dict'):
        try:
            json_data = task_output.json_dict
            topic_objects = json_data.get('topics', [])
            topics = [t.get('topic_name') for t in sorted(topic_objects, key=lambda x: x.get('order', 0))]
            if topics:
                return topics
        except Exception as e:
            print(f"   ⚠️  Warning: Could not parse structured output: {e}")
            print("   Falling back to text parsing...")
    
    # Fallback: Parse as text
    curriculum_text = str(task_output.raw) if hasattr(task_output, 'raw') else str(task_output)
    
    # Try multiple regex patterns
    patterns = [
        r'^\d+\.\s+\*\*([^*]+)\*\*',
        r'^#{1,3}\s+\d+\.\s+(.+?)(?:\s*\(|$)',
        r'^\d+\.\s+([^\(]+)'
    ]
    
    for line in curriculum_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                topic = match.group(1).strip().rstrip('*').strip()
                if topic and len(topic) > 3:
                    topics.append(topic)
                break
    
    return topics


def get_user_approval(topics: List[str]) -> bool:
    """
    Display proposed topics and get user approval (HITL).
    
    Args:
        topics: List of proposed learning topics
        
    Returns:
        True if user approves, False otherwise
    """
    print_section("📋 Proposed Learning Curriculum")
    
    print("The Principal Agent has analyzed your career goal and proposes")
    print("the following topics for your month-long learning journey:\n")
    
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    print(f"\n{'─' * 80}")
    print(f"\nTotal topics: {len(topics)}")
    print("This curriculum will take approximately one month to complete.\n")
    
    while True:
        response = input("Do you approve this curriculum? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("\n📝 Curriculum not approved.")
            print("Please restart the application with a refined career goal.")
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def process_topic(topic: str, topic_num: int, total_topics: int) -> bool:
    """Process single topic through ContentGenerationCrew.
    
    Args:
        topic: Topic to process
        topic_num: Current topic number for display
        total_topics: Total number of topics for display
        
    Returns:
        True if successful, False otherwise
    """
    print_section(f"Processing Topic {topic_num}/{total_topics}: {topic}")
    
    try:
        print("   ➤ Initializing content generation crew...")
        content_crew = ContentGenerationCrew(topic)
        
        print(f"   ➤ Generating educational content for '{topic}'...")
        print("   ⏳ This may take a few minutes...\n")
        
        content_crew.kickoff()
        
        print("\n   ➤ Saving generated content...")
        save_content_outputs(topic, content_crew.crew)
        
        print(f"\n   ✅ Successfully processed: {topic}\n")
        return True
        
    except Exception as e:
        print(f"\n   ❌ Error processing topic '{topic}': {str(e)}")
        print("   Continuing with remaining topics...\n")
        return False


def main() -> None:
    """Main application entry point with two-level crew orchestration."""
    try:
        # Validate API key
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("\n❌ Error: OPENAI_API_KEY not found in environment.")
            print("Please ensure your .env file contains a valid OpenAI API key.\n")
            sys.exit(1)
        
        if not api_key.startswith('sk-'):
            print("\n⚠️  Warning: OPENAI_API_KEY format looks incorrect.")
            print("OpenAI API keys typically start with 'sk-'")
            print("Current value starts with:", api_key[:10] if len(api_key) >= 10 else api_key)
            print("\nPlease verify your API key in the .env file.\n")
            sys.exit(1)
        
        # Step 1: Get user input
        user_name, career_goal = get_user_input()
        
        # Step 2: Generate curriculum
        print_section("🧠 Analyzing Career Goal & Designing Curriculum")
        print("The Principal Agent is analyzing your goal and designing a curriculum...")
        print("This may take a minute...\n")
        
        curriculum_crew = CurriculumCrew(user_name, career_goal)
        curriculum_crew.kickoff()
        
        print("✓ Curriculum proposal generated!\n")
        
        # Step 3: Parse topics
        topics = parse_topics_from_output(curriculum_crew)
        
        if not topics:
            print("❌ Error: Could not parse topics from curriculum output.")
            print("This might be a formatting issue. Please check output/curriculum_proposal.md")
            sys.exit(1)
        
        # Step 4: Get user approval (HITL)
        if not get_user_approval(topics):
            sys.exit(0)
        
        # Step 5: Generate content for each approved topic
        print_banner("🎬 Starting Content Generation", "=")
        print(f"Processing {len(topics)} topics. This will take some time...")
        print("Each topic requires multiple AI agents to collaborate.\n")
        
        successful = 0
        failed = 0
        
        for i, topic in enumerate(topics, 1):
            if process_topic(topic, i, len(topics)):
                successful += 1
            else:
                failed += 1
        
        # Step 6: Summary
        print_banner("✨ Content Generation Complete!", "=")
        
        print("Summary:")
        print(f"  • Total topics: {len(topics)}")
        print(f"  • Successfully processed: {successful}")
        print(f"  • Failed: {failed}")
        print(f"\n  📁 All content saved to: {Config.OUTPUT_DIR}")
        
        print(f"\n{'─' * 80}")
        print("Next Steps:")
        print("  1. Review the generated content in the output/ directory")
        print("  2. Slides are in Markdown format - convert them using Marp or reveal.js")
        print("  3. Search for the suggested video topics on YouTube")
        print("  4. Take the quizzes to assess your understanding")
        print("  5. Follow the lesson plans at your own pace")
        print(f"{'─' * 80}\n")
        
        print(f"Good luck with your learning journey, {user_name}! 🚀\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        print("Your progress has been saved to the output/ directory.\n")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("\n📋 Full error details:")
        traceback.print_exc()
        print("\nPlease check your configuration and try again.")
        print("If the problem persists, review the error details above.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
