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

## Core Feature Spotlight: User Management Architecture

To ensure clarity, stability, and maintainability, User Management (including registration, authentication, and profile management) is treated as a **core, foundational feature** of the application. It is therefore implemented within the **layered API (`/api/v1`) structure**, rather than as a pluggable module in `app/modules`.

This approach ensures that critical user-related functionalities are stable, versioned, and tightly integrated into the application's core business logic.

The user management logic is distributed across the following key files and directories, adhering to the principle of separation of concerns:

*   **`app/api/v1/endpoints/auth.py` (New)**:
    *   **Purpose**: Handles all authentication-related API endpoints, such as user registration (`POST /auth/register`) and user login/token generation (`POST /auth/token`).
    *   **Responsibility**: Receives HTTP requests, validates input, and delegates business logic to `user_service`.

*   **`app/api/v1/endpoints/users.py` (Modified)**:
    *   **Purpose**: Handles API endpoints for managing an authenticated user's own profile information.
    *   **Responsibility**: Provides endpoints like `GET /users/me` (retrieve current user's profile) and `PUT /users/me` (update current user's profile).

*   **`app/services/user_service.py` (Modified)**:
    *   **Purpose**: Contains the core business logic for user management.
    *   **Responsibility**: Orchestrates operations like creating users, retrieving user details, updating user information, and interacting with the `user_repository` and `security` utilities.

*   **`app/db/repositories/user_repository.py` (New)**:
    *   **Purpose**: Encapsulates all direct database interactions for the `User` model.
    *   **Responsibility**: Provides methods for creating, retrieving (by ID, email, username), updating, and deleting `User` records from the database. It abstracts the database specifics from the service layer.

*   **`app/db/models/user.py` (Modified)**:
    *   **Purpose**: Defines the SQLAlchemy ORM model for the `User` entity, mapping it to the `users` table in the database.
    *   **Responsibility**: Specifies the structure and fields of a user record.

*   **`app/api/v1/schemas/user_schemas.py` (Modified)**:
    *   **Purpose**: Defines Pydantic schemas for validating user-related request bodies and structuring API responses.
    *   **Responsibility**: Includes schemas for `UserCreate` (with password), `UserUpdate`, `User`, etc.

*   **`app/core/security.py` (Modified)**:
    *   **Purpose**: Centralizes security-related utilities.
    *   **Responsibility**: Handles password hashing and verification, as well as JWT token creation and decoding.

This structured approach ensures a clear separation of concerns, enhances maintainability, and provides a robust foundation for user management within the application. The `app/modules/user` directory will be removed to avoid architectural ambiguity.