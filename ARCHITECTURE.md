# Architecture Documentation

## System Overview

The Agentic Educational System is a hierarchical multi-agent system designed to generate personalized learning curricula. This document provides detailed architectural insights for technical audiences.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Command Line Interface)                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ User Input (Name, Career Goal)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Main Orchestrator                           │
│                      (app/main.py)                               │
│                                                                   │
│  • Input validation                                              │
│  • Crew instantiation                                            │
│  • Output management                                             │
│  • Error handling                                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Kickoff
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Level 1: CurriculumCrew                        │
│                   (Strategic Planning)                           │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              PrincipalAgent                              │   │
│  │  • Analyzes career goals                                │   │
│  │  • Designs learning path                                │   │
│  │  • Determines topics                                     │   │
│  │  • Allocates time                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           │ Task: topic_identification_task      │
│                           ▼                                      │
│                  Output: List of Topics                          │
│                  (curriculum_proposal.md)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Output
                           ▼
                    ┌──────────────┐
                    │     HITL     │ ◄── Human-in-the-Loop Validation
                    │  (User Gate) │
                    └──────┬───────┘
                           │ Approved?
                           │ Yes
                           ▼
                    ┌──────────────┐
                    │  For Each    │
                    │    Topic     │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Level 2: ContentGenerationCrew                      │
│              (Tactical Execution - Per Topic)                    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 1: Lesson Planning                                  │   │
│  │  ┌──────────────────┐                                    │   │
│  │  │  TeacherAgent    │ → lesson_planning_task             │   │
│  │  │  • Break topics  │   Output: Lesson Plan              │   │
│  │  │    into lessons  │                                    │   │
│  │  └──────────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           │ Context                              │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 2: Slides Creation                                  │   │
│  │  ┌──────────────────┐                                    │   │
│  │  │  SlidesAgent     │ → slides_creation_task             │   │
│  │  │  • Transform to  │   Input: Lesson Plan               │   │
│  │  │    presentations │   Output: Markdown Slides          │   │
│  │  └──────────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 3: Video Suggestions (Parallel)                     │   │
│  │  ┌──────────────────┐                                    │   │
│  │  │  VideoAgent      │ → video_generation_task            │   │
│  │  │  + Custom Tool   │   Input: Lesson Plan               │   │
│  │  │  • Generate      │   Output: Video Suggestions        │   │
│  │  │    video list    │   Tool: HypotheticalVideoSearch    │   │
│  │  └──────────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           │ Context                              │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 4: Quiz Creation                                    │   │
│  │  ┌──────────────────┐                                    │   │
│  │  │  TestAgent       │ → quiz_creation_task               │   │
│  │  │  • Create        │   Input: Slides                    │   │
│  │  │    assessments   │   Output: Quiz + Answer Key        │   │
│  │  └──────────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│                Complete Content Bundle                           │
│          (Lesson Plan + Slides + Videos + Quiz)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Save
                           ▼
                  ┌────────────────┐
                  │ Output Storage │
                  │  (File System) │
                  │                │
                  │  output/       │
                  │  ├─ Topic_1/   │
                  │  ├─ Topic_2/   │
                  │  └─ ...        │
                  └────────────────┘
```

## Component Responsibilities

### 1. Main Orchestrator (app/main.py)
- **Purpose**: Application entry point and workflow controller
- **Responsibilities**:
  - User input/output handling
  - Crew lifecycle management (creation, execution, cleanup)
  - Human-in-the-loop validation
  - Error handling and user feedback
  - Output file management
- **Key Functions**:
  - `get_user_input()`: Gathers user information
  - `create_curriculum_crew()`: Instantiates Level 1 crew
  - `create_content_generation_crew()`: Instantiates Level 2 crews
  - `process_topic()`: Executes content generation for one topic
  - `parse_topics_from_output()`: Extracts topics from LLM output

### 2. Configuration Layer (config/config.py)
- **Purpose**: Centralized configuration management
- **Features**:
  - Environment variable loading (python-dotenv)
  - API key validation
  - Output path management
  - Global constants
- **Design Pattern**: Singleton configuration class
- **Benefits**: Single source of truth for all configuration

### 3. Agent Layer (agents/agents.py)
- **Purpose**: Define intelligent agent personas
- **Agents**:
  - **PrincipalAgent**: Strategic curriculum designer
  - **TeacherAgent**: Lesson plan specialist
  - **SlidesAgent**: Presentation designer
  - **VideoAgent**: Resource curator (with custom tool)
  - **TestAgent**: Assessment creator
- **Design Pattern**: Factory pattern for agent creation
- **Key Attributes**: role, goal, backstory, tools, llm

### 4. Task Layer (agents/tasks.py)
- **Purpose**: Define atomic work units with dependencies
- **Tasks**:
  - **topic_identification_task**: Curriculum generation
  - **lesson_planning_task**: Detailed lesson creation
  - **slides_creation_task**: Presentation generation
  - **video_generation_task**: Resource suggestion
  - **quiz_creation_task**: Assessment creation
- **Design Pattern**: Factory pattern with context chaining
- **Key Features**: expected_output, context, agent assignment

### 5. Tools Layer (tools/video_generation_tool.py)
- **Purpose**: Custom LLM-powered capabilities
- **Tool**: HypotheticalVideoSearchTool
- **Design Rationale**: Since external APIs are not allowed, this tool demonstrates using the LLM's internal knowledge to simulate external data sources
- **Implementation**: CrewAI @tool decorator
- **Key Feature**: Explicit documentation of limitations

## Data Flow

### Phase 1: Curriculum Generation
```
User Input
    ↓
PrincipalAgent analyzes career goal
    ↓
Generates list of 8-12 topics
    ↓
Saves to curriculum_proposal.md
    ↓
Parses topics from markdown
    ↓
Presents to user for approval
```

### Phase 2: Content Generation (Per Topic)
```
Topic name
    ↓
TeacherAgent creates lesson plan
    ↓ (context)
SlidesAgent transforms to slides
    ↓ (context)
VideoAgent suggests videos (using tool)
    ↓
TestAgent creates quiz (from slides)
    ↓
Combine all outputs
    ↓
Save to output/TOPIC_NAME/complete_content.md
```

## Key Design Patterns

### 1. Hierarchical Crew Pattern
- **Level 1 (Strategic)**: High-level planning and decision-making
- **Level 2 (Tactical)**: Detailed execution and content creation
- **Benefit**: Clear separation of concerns, scalable architecture

### 2. Human-in-the-Loop (HITL)
- **Location**: Between Level 1 and Level 2
- **Purpose**: User validation gate
- **Benefit**: Prevents wasted computation, builds trust

### 3. Context Chaining Pattern
```python
task_B.context = [task_A]  # Task B receives Task A's output
task_C.context = [task_B]  # Task C receives Task B's output
```
- **Benefit**: Ensures coherence and alignment across outputs

### 4. Dynamic Crew Instantiation
```python
for topic in approved_topics:
    crew = create_content_generation_crew(topic)
    crew.kickoff(inputs={'topic': topic})
```
- **Benefit**: Each topic is independent, enabling future parallelization

### 5. Factory Pattern
- Used for both agents and tasks
- **Benefit**: Centralized configuration, easy modification

## Scalability Considerations

### Current Architecture (Sequential)
- Topics processed one at a time
- Suitable for: Single user, development/testing

### Future: Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_topic, topic, i, total)
               for i, topic in enumerate(topics, 1)]
    results = [f.result() for f in futures]
```
- Process multiple topics simultaneously
- Reduce total execution time
- Requires: Rate limiting, error handling improvements

### Future: Multi-User Support
- Add user session management
- Database for curriculum storage
- API layer (FastAPI/Flask)
- Job queue (Celery/RQ) for async processing

## Error Handling Strategy

### Levels of Error Handling

1. **Configuration Errors** (Fail Fast)
   ```python
   Config.validate()  # Raises ValueError if API key missing
   ```

2. **Topic Processing Errors** (Graceful Degradation)
   ```python
   try:
       process_topic(topic)
   except Exception as e:
       log_error(e)
       continue  # Continue with remaining topics
   ```

3. **User Interruption** (Clean Exit)
   ```python
   except KeyboardInterrupt:
       save_progress()
       sys.exit(0)
   ```

## Testing Strategy

### Unit Tests (tests/test_tools.py)
- Test individual components in isolation
- Mock external dependencies (LLM calls)
- Fast, deterministic, no API costs

### Integration Tests (tests/test_crews.py)
- Test crew orchestration logic
- Mock crew.kickoff() returns
- Verify agent/task composition
- Validate data flow

### Testing Philosophy
- **No Real API Calls**: All LLM interactions mocked
- **Cost-Effective**: Tests run without incurring API charges
- **Fast**: Complete test suite runs in seconds
- **Deterministic**: Same inputs always produce same results

## Configuration Management

### Environment Variables (.env)
```bash
OPENAI_API_KEY=sk-...
```

### Configuration Class (config.py)
```python
class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_MODEL = 'gpt-4'
    OUTPUT_DIR = Path('output')
    VERBOSE = True
```

### Benefits
- Centralized configuration
- Early validation
- Easy to modify and extend
- Follows 12-factor app principles

## Output Management

### Directory Structure
```
output/
├── curriculum_proposal.md
├── Python_Fundamentals/
│   └── complete_content.md
├── Data_Structures/
│   └── complete_content.md
└── Web_Development/
    └── complete_content.md
```

### File Naming Strategy
- Topic names sanitized for filesystem compatibility
- Special characters replaced with underscores
- Spaces converted to underscores
- Lowercase for consistency

### Future Enhancement: Structured Output
```
output/
└── Python_Fundamentals/
    ├── lesson_plan.md
    ├── slides.md
    ├── videos.md
    └── quiz.md
```

## Performance Considerations

### Current Performance
- Curriculum generation: ~30-60 seconds
- Content per topic: ~2-4 minutes
- Total for 8 topics: ~20-35 minutes

### Optimization Opportunities
1. **Parallel Processing**: Process topics concurrently
2. **Caching**: Cache common curriculum patterns
3. **Streaming**: Stream output as it's generated
4. **Model Selection**: Use GPT-3.5 for less critical tasks

## Security Considerations

### API Key Management
- Never commit .env to version control
- Use environment variables only
- Validate key at startup
- Clear error messages without exposing keys

### Input Validation
- Sanitize file paths
- Validate user input
- Prevent path traversal attacks
- Limit input lengths

### Output Safety
- Sanitize topic names for file systems
- Validate output directories
- Prevent overwriting system files

## Monitoring and Observability

### Current Approach
- Console output with progress indicators
- Error messages with context
- Verbose mode for debugging

### Future Enhancements
- Structured logging (JSON logs)
- Metrics collection (topic count, duration, API calls)
- Error tracking (Sentry, Rollbar)
- Performance monitoring (execution time per stage)

## Conclusion

This architecture demonstrates production-grade design principles:
- **Modularity**: Clear separation of concerns
- **Scalability**: Dynamic crew instantiation supports growth
- **Reliability**: Comprehensive error handling
- **Testability**: Mocked tests for fast, cost-effective validation
- **Maintainability**: Clean code structure with thorough documentation
- **User-Centric**: HITL validation ensures user satisfaction

The hierarchical crew pattern is particularly powerful for complex workflows requiring both strategic planning and detailed execution.
