# Quick Start Guide

## Setup (5 minutes)

1. **Install Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   # OPENAI_API_KEY=sk-...
   ```

## Running the System

```bash
python app/main.py
```

## Example Interaction

```
What's your name? Jane Doe

Please describe your career goal:
Your career goal: Transition from web development to machine learning engineering

[System generates curriculum...]

Proposed Learning Curriculum:
  1. Python for Machine Learning
  2. Mathematics for ML
  3. Supervised Learning Algorithms
  4. Deep Learning Fundamentals
  5. MLOps and Deployment
  ...

Do you approve this curriculum? (yes/no): yes

[System generates content for each topic...]
✓ Content saved to: output/Python_for_Machine_Learning/
...
```

## Testing

```bash
# Install dev dependencies
pip install -r requirements-devel.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agents --cov=tools --cov=app
```

## Output Structure

After running, you'll find:
```
output/
├── curriculum_proposal.md           # Initial curriculum
├── Topic_1_Name/
│   └── complete_content.md         # Lessons, slides, videos, quiz
├── Topic_2_Name/
│   └── complete_content.md
...
```

## Common Issues

### Issue: "OPENAI_API_KEY not found"
**Solution**: Make sure you created `.env` file and added your API key

### Issue: "Module not found"
**Solution**: Activate your virtual environment and reinstall requirements

### Issue: Tests failing
**Solution**: Install dev dependencies: `pip install -r requirements-devel.txt`

## Cost Estimation

Each curriculum generation costs approximately:
- Curriculum planning: ~$0.10-0.30
- Per topic content: ~$0.50-1.50
- Total for 8 topics: ~$5-15 (depending on complexity and length)

## Next Steps

1. Review generated content in `output/` directory
2. Convert slides to presentations (use Marp, reveal.js, or Slidev)
3. Search YouTube for the suggested video topics
4. Take the quizzes to test your understanding
5. Customize agents and tasks for your specific needs

## Architecture Overview

```
User Input → CurriculumCrew (PrincipalAgent)
          → User Approval (HITL)
          → For each topic:
             ContentGenerationCrew:
               ├── TeacherAgent (lesson plan)
               ├── SlidesAgent (presentation)
               ├── VideoAgent (resources)
               └── TestAgent (quiz)
          → Structured Output
```

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review test files for usage examples
3. Examine agent and task definitions for customization
