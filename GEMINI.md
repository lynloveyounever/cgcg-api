# Gemini Context: CGCG-API

## Project Overview

This is a Python-based web service built using the FastAPI framework. Its original purpose was to query information from a Thinkbox Deadline render farm webservice. 

The application is architected to be modular. The core logic in `main.py` dynamically discovers and registers API endpoints from modules located in the `app/modules` directory. This allows for clean separation of concerns and enables developers to work on new features in isolation.

**Key Technologies:**

- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Testing:** Pytest, HTTPX (via FastAPI's TestClient)
- **Configuration:** Pydantic Settings (`app/core/config.py`)

## Building and Running

### 1. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Run the Server

To run the development server, use the following `uvicorn` command. The `--reload` flag enables hot-reloading on code changes.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once running, the service will be available at `http://127.0.0.1:8000`, with interactive API documentation at `http://127.0.0.1:8000/docs`.

### 3. Run Tests

To execute the test suite, run `pytest` from the project root. The `PYTHONPATH=.` prefix is required to ensure that the test runner can correctly locate the main application module.

```bash
PYTHONPATH=. pytest
```

## Development Conventions

### Modular Routers

The primary convention is the dynamic router system. To add a new set of API endpoints (e.g., for a new feature called "projects"), follow these steps:

1.  Create a new directory: `app/modules/projects`
2.  Create an empty `__init__.py` file inside it.
3.  Create a `router.py` file inside it (`app/modules/projects/router.py`).
4.  In `router.py`, define and export an `APIRouter` instance named `router`:

    ```python
    from fastapi import APIRouter

    router = APIRouter(
        prefix="/projects",
        tags=["projects"],
    )

    @router.get("/")
    async def get_projects():
        return [{"name": "Project X"}]
    ```

The application will automatically detect and register this new router on startup.

### Testing

-   Tests are located in the `/tests` directory.
-   Tests are written as standard functions (e.g., `def test_...`) using FastAPI's synchronous `TestClient`.
-   New features and modules should be accompanied by corresponding tests.

### Configuration

-   Application configuration is managed in `app/core/config.py` using `pydantic-settings`.
-   Configuration can be sourced from environment variables or a `.env` file.
