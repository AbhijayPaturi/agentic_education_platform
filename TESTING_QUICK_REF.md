# Quick Test Reference

## Run Tests

```bash
# Full test suite with coverage
PYTHONPATH=. pytest src/tests/ --cov=src --cov-report=term-missing

# Run specific test file
PYTHONPATH=. pytest src/tests/test_agents.py -v

# Run specific test class
PYTHONPATH=. pytest src/tests/test_agents.py::TestPrincipalAgent -v

# Run specific test
PYTHONPATH=. pytest src/tests/test_agents.py::TestPrincipalAgent::test_create_principal_agent_returns_agent -v

# Run with markers (if added)
PYTHONPATH=. pytest src/tests/ -m "unit" -v

# Run failed tests only
PYTHONPATH=. pytest src/tests/ --lf

# Stop on first failure
PYTHONPATH=. pytest src/tests/ -x

# Show print statements
PYTHONPATH=. pytest src/tests/ -s

# Detailed traceback
PYTHONPATH=. pytest src/tests/ --tb=long
```

## Coverage Reports

```bash
# Terminal report with missing lines
PYTHONPATH=. pytest src/tests/ --cov=src --cov-report=term-missing

# HTML report
PYTHONPATH=. pytest src/tests/ --cov=src --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
PYTHONPATH=. pytest src/tests/ --cov=src --cov-report=xml

# Check minimum coverage threshold
PYTHONPATH=. pytest src/tests/ --cov=src --cov-fail-under=80
```

## Test Structure

```
src/tests/
├── test_config.py              # Configuration tests (9 tests)
├── test_schemas.py             # Pydantic schema tests (19 tests)
├── test_agents.py              # Agent creation tests (25 tests)
├── test_crews_comprehensive.py # Crew orchestration tests (19 tests)
├── test_utils.py               # Utility function tests (15 tests)
└── test_main.py                # Main app logic tests (21 tests)

Total: 108 test cases
Core coverage: 98% (373 statements, 7 missed)
```

## Current Test Status

✅ All 108 tests passing
✅ 98% core-library coverage
✅ Comprehensive edge case testing
✅ Proper mocking for external dependencies
✅ Type hints throughout test code

## Test Categories

- **Unit Tests**: Individual function/class testing
- **Integration Tests**: Crew orchestration and workflow
- **Edge Case Tests**: Empty inputs, special chars, validation errors
- **Error Handling Tests**: API key issues, user interrupts, exceptions
