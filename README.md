# 🎓 Agentic Education Platform

> **Production-grade multi-agent system for personalized curriculum generation using CrewAI**
> **Fun Fact: Used these learning modules to learn how to DJ for my friends this summer**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Core Coverage](https://img.shields.io/badge/core%20coverage-98%25-brightgreen.svg)](./TEST_COVERAGE_REPORT.md)
[![Tests](https://img.shields.io/badge/tests-108%20passing-brightgreen.svg)](./TESTING_QUICK_REF.md)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

## 🎯 Purpose

This project **eliminates the time-consuming process of searching for the "right" educational materials**. Instead of spending hours scrolling through courses, videos, and tutorials, learners receive a comprehensive, personalized curriculum instantly—accelerating knowledge attainment and reducing time-to-competency.

## At a Glance

This portfolio project demonstrates production-oriented AI engineering rather than a
single prompt wrapper: five specialized agents collaborate through validated Pydantic
contracts, a human approval gate controls cost and quality, and every topic produces
both machine-readable data and student-ready learning materials.

| Engineering concern | Implementation |
|---------------------|----------------|
| Orchestration | Strategic curriculum crew followed by a four-agent content crew |
| Reliability | Cross-field validation for durations, counts, and content ordering |
| Student experience | Lessons, slides, live video searches, quiz, and separate answer key |
| Safety | Sanitized paths, environment-based secrets, TLS verification on by default |
| Verification | 108 automated tests with mocked LLM calls |

## Inspiration

I built this project because I wanted a clear, structured learning class that could
teach me how to DJ using freely available resources. My goal was practical and
personal: learn enough to DJ for my friends throughout the summer without paying
for an expensive course or spending hours piecing together disconnected tutorials.

That experience shaped the application around a simple idea: give learners an
organized path, useful practice, trusted resources, and assessments in one place so
they can spend more time building the skill and less time figuring out what to learn
next. The generated learning resources can be free to access, although running the
application itself may incur OpenAI API usage costs.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+ (3.12 recommended)
- Conda (Miniconda or Anaconda)
- OpenAI API key

### 1. Create Conda Environment
```bash
# Create and activate environment
conda create -n agentic_education_platform python=3.12 -y
conda activate agentic_education_platform
```

### 2. Install Dependencies
```bash
# Navigate to project directory
cd agentic_education_platform

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-devel.txt
```

### 3. Configure Environment
```bash
# Copy the template and add your OpenAI API key
cp .env.example .env
# then edit .env and set OPENAI_API_KEY=sk-...
```

The application is configured entirely through environment variables (12-factor style). All settings have safe defaults — only `OPENAI_API_KEY` is required.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ | — | OpenAI API key used by every agent |
| `OPENAI_MODEL` | ❌ | `gpt-4o-mini` | LLM for all agents (e.g. `gpt-4o`, `gpt-4-turbo`) |
| `VERBOSE` | ❌ | `true` | Verbose crew/agent logging |
| `DISABLE_SSL_VERIFY` | ❌ | `false` | Opt-in TLS bypass for corporate proxies (see [Security](#-security-notes)) |

### 4. Run the Application
```bash
# Launch the platform (from the project root)
python run.py

# Equivalent module entry point
python src/app/run.py
```

### 5. Run Test Suite
```bash
# Run all tests with coverage report
pytest src/tests/ --cov=src --cov-report=term-missing
```

**Expected Output:** The system will:
1. Prompt for your name and career goal
2. Generate a personalized curriculum proposal (Level 1)
3. Request approval
4. Generate detailed content for each topic (Level 2)
5. Save all outputs to `output/` directory

### Student Artifacts

Each approved topic gets its own folder with complementary formats:

| Artifact | Purpose |
|----------|---------|
| `lesson_plan.md` / `.json` | Progressive lessons, objectives, timing, and activities |
| `slides.md` / `.json` | Self-paced presentation with examples and speaker notes |
| `video_resources.md` / `.json` | Reputable channels and working YouTube search links |
| `quiz.md` | Student assessment without visible answers |
| `quiz_answer_key.md` | Separate answers and explanations for review |
| `quiz.json` | Complete structured assessment for future UI/LMS integrations |
| `complete_content.md` | Consolidated raw backup of all agent outputs |

Try the API-free structured-output example with:

```bash
python -m examples.schema_usage_example
```

---

## 🏗️ Architecture & Design Logic

### Production-Grade Design Principles

#### 1. **Two-Level Agent Orchestration**
The system employs a **strategic-tactical decomposition** pattern:

**Level 1: Strategic Planning (CurriculumCrew)**
- Single Principal Agent analyzes career goals
- Produces high-level 4-6 topic curriculum
- Validates total duration (20-35 days)
- Outputs structured JSON schema using Pydantic

**Level 2: Tactical Execution (ContentGenerationCrew)**
- Four specialized agents work sequentially per topic
- Each agent builds on previous outputs
- Ensures consistency and context propagation
- Produces comprehensive educational materials

**Why Sequential Flow?**
- **Context Integrity**: Each agent needs complete output from predecessor
- **Quality Assurance**: Teacher validates before slides/videos/quizzes
- **Deterministic Results**: Reproducible, traceable execution
- **Cost Efficiency**: No wasted parallel API calls on bad inputs

#### 2. **Type-Safe Schema Architecture**
Every agent output is validated through **Pydantic v2** schemas:

```python
CurriculumProposal → LessonPlan → PresentationSlides → VideoResources → Quiz
```

**Benefits:**
- Runtime validation catches errors early
- Self-documenting API contracts
- IDE autocomplete and type checking (mypy)
- Easy serialization to JSON
- Production-ready data integrity

#### 3. **Separation of Concerns**
```
src/
├── agents/          # Agent definitions by role (SRP)
├── crews/           # Orchestration logic
├── config/          # Environment & settings
├── utils/           # Pure functions (formatting, I/O)
├── tools/           # External API integrations
├── tests/           # Comprehensive test suite (98% core coverage)
└── app/             # Entry points
```

**Design Rationale:**
- **Modularity**: Each agent is independently testable
- **Scalability**: Add new agents without touching existing code
- **Maintainability**: Clear boundaries between layers
- **Testability**: Dependency injection via config

#### 4. **Defensive Programming**
- SSL certificate handling for enterprise proxies
- Graceful degradation (structured JSON → markdown parsing)
- Input validation with retry logic
- Comprehensive error handling and logging
- User interrupt handling (Ctrl+C)

---

## 🏆 What Makes This Project Stand Out

### 1. **Production-Ready Code Quality**
- 98% core-library coverage with comprehensive edge cases
- Type-safe architecture (mypy validated)
- Proper error handling and logging
- Defensive programming patterns
- Modular, extensible design

### 2. **Advanced AI Engineering**
- Multi-agent orchestration (not just single LLM calls)
- Schema-driven output validation (production requirement)
- Context management across agent chain
- Tool integration (YouTube search)
- Two-level strategic/tactical decomposition

### 3. **Real-World Problem Solving**
- Solves actual pain point (curriculum creation is time-intensive)
- Practical output formats (JSON + Markdown)
- Human-in-the-loop design (approval gates)
- Cost-conscious (sequential execution)

### 4. **Scalability Vision**
- Clear roadmap to 10x features
- Database integration strategy
- Multi-model orchestration
- API-first architecture (easy to extend)

### 5. **Data Science Best Practices**
- Reproducible results (deterministic flow)
- Experiment tracking potential (MLflow integration)
- A/B testing ready
- Performance metrics (generation time, costs)

### 6. **Enterprise-Ready Architecture**
- Separation of concerns (clean architecture)
- Configuration management (12-factor app)
- Observability hooks (logging, metrics)
- Security considerations (API key management)

---

## 🎯 Next Steps: Scaling to Production

### 1. **Real-Time Internet Search Integration**
Integrate live web search capabilities (SerperDev, Google Custom Search) and content scraping to dynamically source current educational materials.

**Impact:** Fresh content recommendations, automatic link validation, trending topic incorporation, multi-source aggregation (YouTube, Coursera, Udemy, Khan Academy).

### 2. **User Preference Persistence & Memory**
Implement PostgreSQL/MongoDB for user profiles, learning history, and preferences with Redis caching for session management.

**Impact:** Personalized recommendations, progress tracking across sessions, adaptive difficulty adjustment, spaced repetition scheduling, ML-based learning style detection.

### 3. **Multi-Model LLM Orchestration**
Build intelligent routing system that selects optimal LLM (GPT-4, Claude, Gemini, Llama) per task based on performance, cost, and latency.

**Impact:** 40-60% cost reduction, leverage model-specific strengths, automatic fallbacks, A/B testing infrastructure, token usage analytics.

### 4. **Hierarchical Multi-Agent Architecture**
Expand to hierarchical teams with meta-orchestrator coordinating planning, content, and quality assurance teams in parallel workflows.

**Impact:** 50-70% faster generation through parallelization, self-correction loops, consensus-based decisions, scalable to 10+ agents, dynamic task allocation.

### 5. **Enhanced Multimedia Generation**
Integrate DALL-E 3/Stable Diffusion for diagrams, D-ID/Synthesia for video synthesis, ElevenLabs for text-to-speech, creating actual files not just suggestions.

**Impact:** Turnkey PowerPoint files with custom diagrams, auto-generated explainer videos with AI narration, audio lessons, interactive infographics, accessibility features.

### 6. **Interactive Web Platform**
Develop full-stack application with FastAPI backend, React/Next.js frontend, WebSocket for real-time monitoring and collaborative editing.

**Impact:** Browser-based access, real-time progress tracking, collaborative curriculum editing, LMS export (Moodle, Canvas, Blackboard), mobile app, OAuth/SSO integration.

### 7. **Intelligent Adaptive Assessment System**
Implement Computer Adaptive Testing (CAT) that adjusts difficulty in real-time with LLM-based automated grading and feedback.

**Impact:** Accurate competency assessment, reduced test fatigue, automated essay grading, personalized remediation, skills gap analysis, success probability prediction.

### 8. **Social Learning Features**
Add community features: peer matching, mentor connections, discussion forums, collaborative projects, gamification elements.

**Impact:** Increased engagement through social accountability, peer knowledge sharing, expert guidance, leaderboards, community resource library, study group coordination.

### 9. **Enterprise Features & B2B Capabilities**
Build enterprise console for bulk curriculum generation, team skills mapping, compliance training, learning ROI tracking.

**Impact:** Role-based learning paths for organizations, team skills gap identification, automated compliance training, analytics tied to business KPIs, HRIS integration.

### 10. **Advanced Analytics & Predictive Insights**
Implement ML analytics engine tracking engagement patterns, predicting outcomes, recommending interventions before learners fall behind.

**Impact:** Detailed engagement metrics, early warning system for at-risk learners, completion likelihood prediction, personalized schedule optimization, content effectiveness analysis.

### 11. **Content Marketplace & Creator Economy**
Build platform for expert educators to contribute, curate, and monetize specialized content with quality ratings and revenue sharing.

**Impact:** Diverse expert-validated content library, revenue stream for SMEs, community-driven quality improvement, specialized niche coverage, continuous content freshness.

---

## 🧪 Testing Suite

### Coverage Metrics
- **98% coverage of the core library** (373 statements, 7 missed)
- **108 passing tests** across 6 test modules
- **Edge cases**: Unicode, empty inputs, malformed data
- **Error paths**: Missing API keys, invalid formats, user interrupts

> Note: coverage focuses on the deterministic library code. The interactive
> CLI (`src/app`) and import-time config (`src/config`) are exercised via mocked
> flow tests rather than line coverage.

### Test Architecture
```python
test_config.py              # Configuration & environment
test_schemas.py             # Pydantic validation
test_agents.py              # Agent creation & tasks
test_crews_comprehensive.py # Orchestration logic
test_utils.py               # Formatting & I/O
test_main.py                # End-to-end flows
```

**Testing Strategy:**
- **Mocking**: Zero API calls during tests (MagicMock, patch)
- **Parametrization**: DRY test patterns
- **Fixtures**: Reusable test data
- **Integration**: Multi-agent workflow tests

**Quality Tools:**
- `pytest` + `pytest-cov` for testing
- `mypy` for static type checking
- `black` for code formatting
- `flake8` + `ruff` for linting

See [TEST_COVERAGE_REPORT.md](./TEST_COVERAGE_REPORT.md) for detailed analysis.

---

## 🤖 Agents & Task Flow

### Agent Roster

#### 1. **Principal Agent** (Strategic Planner)
- **Role**: Educational Curriculum Architect
- **Goal**: Design optimal learning path based on career goals
- **Output**: `CurriculumProposal` (4-6 topics, 20-35 days)
- **Schema**: Validates topic order, prerequisites, success criteria

#### 2. **Teacher Agent** (Content Creator)
- **Role**: Expert Educator & Lesson Designer
- **Goal**: Create detailed, actionable lesson plans
- **Output**: `LessonPlan` (objectives, lessons, assessments)
- **Schema**: Enforces 3+ objectives, 4+ lessons, Bloom's taxonomy

#### 3. **Slides Agent** (Visual Designer)
- **Role**: Presentation Specialist
- **Goal**: Design engaging slides with speaker notes
- **Output**: `PresentationSlides` (10+ slides, design notes)
- **Schema**: Validates content types, slide structure

#### 4. **Video Agent** (Resource Curator)
- **Role**: Video Learning Specialist (with YouTube search tool)
- **Goal**: Suggest relevant, modern video resources
- **Output**: `VideoResources` (5-8 videos, viewing guide)
- **Schema**: Provides working YouTube search URLs, recommended channels, and difficulty levels

#### 5. **Test Agent** (Assessment Designer)
- **Role**: Assessment Specialist
- **Goal**: Create comprehensive quizzes
- **Output**: `Quiz` (10+ questions, multiple types)
- **Schema**: Validates question types, difficulty distribution

### Sequential Task Flow

```
User Input (Name + Career Goal)
        ↓
┌─────────────────────────────────────┐
│  LEVEL 1: Strategic Planning       │
│  ┌───────────────────────────────┐ │
│  │  Principal Agent              │ │
│  │  Task: Topic Identification   │ │
│  │  Output: CurriculumProposal   │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
        ↓
   User Approval?
        ↓ (yes)
┌─────────────────────────────────────┐
│  LEVEL 2: Tactical Execution       │
│  (Repeated for each topic)          │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  1. Teacher Agent             │ │
│  │     → LessonPlan              │ │
│  └───────────────────────────────┘ │
│         ↓ (context passed)          │
│  ┌───────────────────────────────┐ │
│  │  2. Slides Agent              │ │
│  │     → PresentationSlides      │ │
│  └───────────────────────────────┘ │
│         ↓ (context passed)          │
│  ┌───────────────────────────────┐ │
│  │  3. Video Agent               │ │
│  │     → VideoResources          │ │
│  └───────────────────────────────┘ │
│         ↓ (context passed)          │
│  ┌───────────────────────────────┐ │
│  │  4. Test Agent                │ │
│  │     → Quiz                    │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
        ↓
Save to output/{topic_name}/
  - lesson_plan.json, .md
  - slides.json, .md
  - video_resources.json, .md
  - quiz.json, .md
        - quiz_answer_key.md
  - complete_content.md
```

**Why This Flow Works:**
1. **Human-in-the-Loop**: User approves strategy before execution
2. **Context Accumulation**: Each agent sees all previous outputs
3. **Progressive Refinement**: Later agents can reference earlier work
4. **Failure Isolation**: Topic-level failures don't crash entire curriculum

---

## 🔌 APIs & Technologies

### Core Stack
| Technology | Purpose | Version |
|------------|---------|---------|
| **CrewAI** | Multi-agent orchestration | ≥0.28.0 |
| **OpenAI** | LLM reasoning engine (model configurable) | via API |
| **Pydantic** | Schema validation | ≥2.0.0 |
| **Python** | Runtime environment | 3.10+ (3.12 recommended) |

### Integration Points
- **OpenAI API**: All agent reasoning; model set via `OPENAI_MODEL` (default `gpt-4o-mini`)
- **YouTube Search**: Working search URLs for video resources (custom tool)
- **File I/O**: Structured output persistence (JSON + Markdown)

### Configuration Management
- **python-dotenv**: Environment variable loading (12-factor)
- **Opt-in SSL bypass**: Enterprise proxy support, disabled by default
- **Path management**: Cross-platform compatibility

---

## 🔒 Security Notes

- **API keys** are read from the environment via `.env` (git-ignored) and never hard-coded.
- **Filesystem safety**: all user-provided text (topics, career goals) is passed through a single `sanitize_filename` helper before being used in paths, preventing path traversal into or out of the `output/` directory.
- **TLS verification is ON by default.** Certificate validation is only disabled when you explicitly set `DISABLE_SSL_VERIFY=true` — intended solely for corporate networks that intercept HTTPS with self-signed certificates. Leave it off on untrusted networks.
- **Telemetry** (CrewAI / OpenTelemetry) is disabled by default to avoid background network calls.

---

## 📝 Project Structure
```
agentic_education_platform/
├── src/
│   ├── agents/           # 5 specialized agents
│   │   ├── principal/    # Curriculum architect
│   │   ├── teacher/      # Lesson designer
│   │   ├── slides/       # Presentation creator
│   │   ├── video/        # Resource curator
│   │   └── test/         # Assessment builder
│   ├── crews/            # Orchestration logic
│   │   ├── curriculum_crew.py       # Level 1
│   │   └── content_generation_crew.py # Level 2
│   ├── config/           # Environment & settings
│   ├── tools/            # External integrations
│   ├── utils/            # Helper functions
│   ├── tests/            # 108 test cases (98% core coverage)
│   └── app/              # Entry points
├── output/               # Generated curricula
├── requirements.txt      # Production dependencies
├── requirements-devel.txt # Dev tools
├── pyproject.toml        # Project metadata
├── .env                  # API keys (gitignored)
├── TEST_COVERAGE_REPORT.md
├── TESTING_QUICK_REF.md
└── README.md             # This file
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent framework
- **OpenAI**: LLM infrastructure
- **Pydantic**: Data validation
- **Python Community**: Testing and tooling ecosystem

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities:
- **Documentation**: See `ARCHITECTURE.md`, `TEST_COVERAGE_REPORT.md`
- **Testing Guide**: See `TESTING_QUICK_REF.md`

---

**Built with ❤️ for learners everywhere. Powered by AI, validated by tests, designed for scale.**
