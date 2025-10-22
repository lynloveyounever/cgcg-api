 [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/lynloveyounever/cgcg-api.git&ephemeral=true&show=ide)

# CGCG API

A robust and scalable API built with FastAPI, featuring a hybrid architecture that combines a professional, layered structure with a pluggable modular system.

## Features

- **Hybrid Architecture**: Core business logic is built on a clean, layered architecture (`api/v1`, `services`, `db`), while a separate `modules` system allows for rapid development and extension of self-contained features.
- **Configuration-Driven**: Application settings and module loading are controlled via Pydantic settings in `app/core/config.py`.
- **Versioning**: The primary API is versioned under `/api/v1`.
- **Pluggable Modules**: Easily enable, disable, or develop new features as self-contained modules (e.g., `deadline`, `media_shuttle`, `user`).
- **Testing**: Comprehensive test suite using `pytest`.
- **Containerization**: Ready for deployment with a provided `Dockerfile`.

## Architecture Overview

This project employs a hybrid architecture to maximize both robustness and development speed:

1.  **Layered API (`app/api/v1`)**: A professional structure separating concerns into `endpoints`, `schemas`, `services`, and `repositories`. This is the recommended structure for core, stable features.
2.  **Pluggable Modules (`app/modules`)**: A simpler, self-contained structure for features that can be easily added or removed. The application dynamically loads routers from enabled modules listed in the configuration.

Both systems are integrated in `main.py` and run side-by-side.

## Getting Started

### Prerequisites

- Python 3.12+
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd cgcg-api
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file by copying the example. (This project does not yet require any specific variables, but it is good practice).
    ```bash
    cp .env.example .env
    ```

## Running the Application

To run the development server with live reloading:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running Tests

To run the full test suite:

```bash
./run_tests.sh
```

## API Documentation

Once the server is running, interactive API documentation (Swagger UI) is available at:

- **http://127.0.0.1:8000/docs**

And alternative documentation (ReDoc) is available at:

- **http://127.0.0.1:8000/redoc**
