# Project Structure & Organization

## Root Level
```
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Tool configurations (Black, Ruff)
├── Dockerfile          # Container configuration
├── run_tests.sh        # Test execution script
├── README.md           # Project documentation
└── .env                # Environment variables (create from .env.example)
```

## Application Structure (`app/`)

### Hybrid Architecture Overview
The project uses two complementary architectural patterns:

1. **Layered API** (`app/api/v1/`) - Professional structure for core features
2. **Pluggable Modules** (`app/modules/`) - Self-contained features

### Core Directories

```
app/
├── __init__.py
├── api/v1/             # Versioned API endpoints (layered architecture)
│   ├── endpoints/      # Route handlers
│   ├── schemas/        # Pydantic models for request/response
│   └── api_router.py   # Main router aggregation
├── core/               # Application core components
│   ├── config.py       # Pydantic settings configuration
│   ├── dependencies.py # FastAPI dependencies
│   ├── exceptions.py   # Custom exception handlers
│   └── security.py     # Authentication/authorization
├── db/                 # Database layer
│   ├── models/         # Database models
│   ├── repositories/   # Data access layer
│   └── session.py      # Database session management
├── services/           # Business logic layer
│   ├── base.py         # Base service class
│   └── *_service.py    # Feature-specific services
└── modules/            # Pluggable feature modules
    ├── deadline/       # Self-contained deadline feature
    ├── media_shuttle/  # Self-contained media shuttle feature
    └── user/           # Self-contained user feature
```

## Testing Structure (`tests/`)
```
tests/
├── test_main.py        # Main application tests
├── test_*.py           # Feature-specific tests
└── conftest.py         # Pytest configuration (if needed)
```

## Architectural Patterns

### Layered API Pattern (`app/api/v1/`)
Use for core, stable features requiring:
- Clear separation of concerns
- Professional structure
- Long-term maintainability

### Module Pattern (`app/modules/`)
Use for features that need:
- Rapid development
- Easy enable/disable capability
- Self-contained functionality
- Experimental features

## Naming Conventions

- **Files**: snake_case (e.g., `user_service.py`)
- **Classes**: PascalCase (e.g., `UserService`)
- **Functions/Variables**: snake_case (e.g., `get_user_by_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Modules**: snake_case directory names

## Configuration Management

- All settings centralized in `app/core/config.py`
- Use Pydantic Settings for type safety
- Environment variables loaded from `.env` file
- Module-specific settings included in main Settings class