# Gemini Project Context

This document summarizes the key aspects of the `cgcg-api` project for the Gemini agent.

## Project Goal

To build a robust, scalable, and professional FastAPI application. The project has been evolved into a hybrid architecture that supports both a strict, layered API structure and a flexible, pluggable module system.

## Key Architecture

- **Hybrid Model**: The application loads two types of routing systems in `main.py`:
  1.  **Layered API (`/api/v1`)**: A professional, versioned API structure located in `app/api/v1`. This is intended for core, stable business logic.
  2.  **Pluggable Modules**: A configuration-driven system that loads self-contained modules from the `app/modules` directory. This allows for rapid development and extension.

## Key Files & Directories

- `main.py`: The main application entrypoint. It initializes the FastAPI app and includes routers from both the layered API and the pluggable modules.
- `app/core/config.py`: Contains Pydantic `Settings` for the application, including the `MODULES` list that controls which pluggable modules are loaded.
- `app/api/v1/api_router.py`: The main router for the v1 layered API. It aggregates all endpoints from `app/api/v1/endpoints/`.
- `app/modules/`: Directory for self-contained, pluggable features. Each module typically has its own `router.py`, `service.py`, and `schemas.py`.
- `app/db/`, `app/services/`: Directories for the layered architecture, containing database models, repositories, and business logic services.
- `tests/`: Contains the `pytest` test suite.
- `run_tests.sh`: The primary script for running the test suite.
- `pyproject.toml`: Defines project metadata and tool configurations (e.g., `black`, `ruff`).
- `Dockerfile`: Defines the container for deploying the application.
- `README.md`: The main user-facing documentation for the project.

## Key Commands

- **Run development server**:
  ```bash
  uvicorn main:app --reload
  ```
- **Run test suite**:
  ```bash
  ./run_tests.sh
  ```
- **Install dependencies**:
  ```bash
  pip install -r requirements.txt
  ```