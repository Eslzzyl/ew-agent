# AGENTS.md

This file contains guidelines for agentic coding agents working in this repository.

## Build & Development Commands

Always use `uv` to run Python files. NEVER directly use `python` or `python3`.

### Running the Application
```bash
uv run main.py
```

### Linting & Formatting
```bash
# Check code style
ruff check .

# Auto-fix linting issues
ruff check . --fix

# Format code
ruff format .
```

### Database

- SQLite database auto-created at `data/eat_what.db` on first run
- Initialized via `models.init_db()` in main.py

## Code Style Guidelines

### Imports

- Standard library imports first, then third-party, then local imports
- Separate groups with blank lines
- No wildcard imports
- Example:
```python
import os
from datetime import datetime
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAILike
from sqlalchemy import Column, Integer, String

from models import FoodChoice, SessionLocal
```

### Type Hints
- Use type hints for function arguments and return values
- Import from `typing` module: `Optional`, `List`, `Dict`, etc.
- Annotate database session type: `db: Session = SessionLocal()`

### Naming Conventions
- Snake_case for variables, functions, and modules
- PascalCase for classes (SQLAlchemy models)
- UPPER_CASE for constants
- Descriptive names for database tables and columns

### Error Handling
- Use try/except/finally pattern for database operations
- Always rollback on exceptions and close sessions in finally blocks
- Return error messages as strings for tool functions
- Example:
```python
db: Session = SessionLocal()
try:
    db.add(item)
    db.commit()
    return "Success"
except Exception as e:
    db.rollback()
    return f"Error: {str(e)}"
finally:
    db.close()
```

### Docstrings
- Use triple-quoted docstrings for all functions
- Include Args and Returns sections for tool functions
- Write docstrings and comments in Chinese
- Example:
```python
@tool
def get_current_time() -> str:
    """获取当前系统时间并判断餐次类型

    Returns:
        当前时间和餐次类型（早饭、午饭、晚饭、其他）
    """
```

### Database Patterns
- Use SQLAlchemy ORM with declarative base
- Define relationships with `relationship()` and `back_populates`
- Use cascade delete for related records
- Index frequently queried fields
- Use `func` for aggregations in queries

### Tool Functions
- Decorate with `@tool` from agno.tools
- Return human-readable strings as results
- Use Optional parameters for non-required arguments
- Keep functions focused and single-purpose

### Environment Variables
- Use `python-dotenv` to load `.env` file
- Access via `os.getenv()` with defaults
- Common vars: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `MODEL_NAME`

### Agent Configuration
- Define instructions as multi-line strings
- Add tools to agent tools list
- Enable context features: `add_datetime_to_context`, `add_history_to_context`
- Support markdown output

### File Organization
- `models.py`: SQLAlchemy models and database setup
- `tools.py`: Tool functions decorated with @tool
- `agent.py`: Agent configuration
- `main.py`: CLI entry point
- Keep database operations in tools.py
- Keep agent logic in agent.py

## Testing
- No test framework currently configured
- To add tests, install pytest and create test files
