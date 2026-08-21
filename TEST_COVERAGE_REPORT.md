# Test Coverage Report

## Verified Result

Measured on Python 3.12 with `pytest`, `pytest-cov`, and no network calls:

- **108 tests passed**
- **98% core-library coverage**
- **373 statements measured; 7 missed**
- **0 external API calls** (CrewAI and user interactions are mocked)

Run the same check with:

```bash
conda run -n agentic_education_platform python -m pytest src/tests/ -q
```

## Scope

Coverage is intentionally reported as **core-library coverage**. The current
`pyproject.toml` excludes `src/app/*` and `src/config/*` from the percentage
because those modules contain interactive CLI and environment/import behavior.
Their flows are still exercised by mocked tests in `test_main.py` and
`test_config.py`; they are simply not included in the headline line metric.

| Area | Tests | What is verified |
|------|------:|------------------|
| Agents and tasks | 25 | Roles, tools, task context, output schemas, safe paths |
| Configuration | 9 | Defaults, validation, output paths, API-key handling |
| Crew orchestration | 19 | Agent/task composition, sequencing, kickoff, outputs |
| CLI flows | 21 | Input retries, parsing, approval, failures, interrupts |
| Pydantic schemas | 19 | Field constraints, totals, counts, contiguous ordering |
| Formatters and I/O | 15 | JSON/Markdown artifacts, separate quiz answer key |
| **Total** | **108** | |

## Core Coverage Detail

| Module group | Coverage |
|--------------|---------:|
| Agent factories | 100% |
| Principal, test, and video schemas | 100% |
| Teacher schema | 97% |
| Slides schema | 95% |
| Crew orchestration | 94-100% |
| Output and text utilities | 99-100% |
| Video resource tool | 62% |
| **Total** | **98%** |

The remaining seven lines are narrow error/branch paths and CrewAI-decorated tool
execution. They do not represent untested external API behavior because the test
suite deliberately makes no paid or nondeterministic network calls.

## Test Principles

- Tests are deterministic and can run in any order.
- Temporary directories isolate all filesystem writes.
- Pydantic tests reject internally inconsistent LLM output before persistence.
- Agent and crew tests mock execution while preserving orchestration contracts.
- CLI tests cover user approval, parse fallbacks, partial failures, and interrupts.

Generate an HTML report locally with:

```bash
conda run -n agentic_education_platform \
  python -m pytest src/tests/ --cov=src --cov-report=html
open htmlcov/index.html
```
