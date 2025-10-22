# Technology Stack & Build System

## Core Technologies

- **Framework**: FastAPI (Python web framework)
- **Python Version**: 3.12+
- **ASGI Server**: Uvicorn for development and production
- **Configuration**: Pydantic Settings with .env file support
- **Testing**: pytest with FastAPI TestClient
- **HTTP Client**: httpx for testing
- **Containerization**: Docker with Python 3.12-slim base image

## Code Quality Tools

- **Formatter**: Black (line length: 88)
- **Linter**: Ruff (E, F, W, I rules enabled)
- **Configuration**: pyproject.toml for tool settings

## Common Commands

### Development
```bash
# Start development server with hot reload
uvicorn main:app --reload

# Server runs on http://127.0.0.1:8000
# API docs available at /docs and /redoc
```

### Testing
```bash
# Run all tests
./run_tests.sh

# Or directly with pytest
PYTHONPATH=. pytest
```

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Docker
```bash
# Build image
docker build -t cgcg-api .

# Run container
docker run -p 8000:8000 cgcg-api
```

## Dependencies

Core dependencies are minimal and focused:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pytest` - Testing framework
- `httpx` - HTTP client for tests
- `pydantic-settings` - Configuration management