# CGCG API Product Overview

CGCG API is a robust and scalable REST API built with FastAPI that serves as a comprehensive backend for CGCG services. The API features a hybrid architecture designed to balance professional development practices with rapid feature development.

## Key Features

- **Hybrid Architecture**: Combines a professional layered structure for core features with a pluggable modular system for rapid development
- **Configuration-Driven**: Application behavior controlled via Pydantic settings
- **API Versioning**: Primary API versioned under `/api/v1`
- **Self-Contained Modules**: Features can be easily enabled, disabled, or developed independently
- **Comprehensive Testing**: Full test coverage using pytest
- **Container Ready**: Dockerized for easy deployment

## Architecture Philosophy

The project uses two complementary approaches:
1. **Layered API** (`app/api/v1`): Professional structure for core, stable features
2. **Pluggable Modules** (`app/modules`): Simpler structure for features that need flexibility

This hybrid approach maximizes both code quality and development velocity.