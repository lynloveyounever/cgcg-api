---
inclusion: always
---

# CGCG API Development Guide

FastAPI-based REST API with hybrid architecture. Follow these patterns and conventions when creating or modifying code.

## Architecture Decision Framework

**Use Layered API** (`app/api/v1/`) when:
- Building core authentication/authorization features
- Creating stable, versioned endpoints
- Implementing complex business logic requiring separation of concerns

**Use Pluggable Modules** (`app/modules/`) when:
- Integrating external services (APIs, message queues)
- Building self-contained features that can be enabled/disabled
- Rapid prototyping or experimental functionality

## Mandatory Code Patterns

### Service Classes
All business logic MUST use async service classes with singleton instances:

```python
class FeatureService:
    async def method_name(self, param: Type) -> ReturnType:
        """Always include docstrings for service methods."""
        # Implementation here
        pass

# Always create singleton at module level
feature_service = FeatureService()
```

### External HTTP Calls
Use this EXACT pattern for all external API requests:

```python
import httpx

async with httpx.AsyncClient() as client:
    try:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return [Schema(**item) for item in response.json()]
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e}")
        return []  # Always return safe defaults, never raise
    except Exception as e:
        print(f"Request failed: {e}")
        return []
```

### Pydantic Schema Conventions
Follow this inheritance hierarchy for all data models:

```python
# 1. Base schema with common fields
class FeatureBase(BaseModel):
    name: str
    description: Optional[str] = None

# 2. Creation schema
class FeatureCreate(FeatureBase):
    pass  # Add creation-specific fields if needed

# 3. Update schema with optional fields
class FeatureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# 4. Database base with ID
class FeatureInDBBase(FeatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 5. Public response schema
class Feature(FeatureInDBBase):
    pass

# 6. Internal database schema with sensitive fields
class FeatureInDB(FeatureInDBBase):
    # Add sensitive fields here if needed
    pass
```

### Message/Task Patterns
For async operations, use the established message/task utilities:

```python
# For background tasks
from app.core.tasks_utils import create_task, get_task_status

# For message publishing
from app.core.messages_utils import publish_message

# Always handle async operations gracefully
task_id = await create_task("operation_name", payload)
```

## File Organization Rules

### Module Structure
Every module in `app/modules/` MUST follow this structure:

```
feature_name/
├── __init__.py     # Export main service and schemas
├── service.py      # Business logic (required)
├── schemas.py      # Pydantic models (required)
├── router.py       # FastAPI routes (optional)
└── message.py      # Message handling (if async operations)
```

### Import Conventions
Always follow this import order:
```python
# Standard library
import asyncio
from typing import Optional, List

# Third-party
from fastapi import HTTPException
from pydantic import BaseModel

# Local imports
from app.core.config import settings
from app.core.security import verify_token
```

## Security Requirements

- **Passwords**: Use `passlib[bcrypt]` for hashing
- **JWT Tokens**: Use `python-jose[cryptography]` 
- **Secrets**: Store in environment variables, access via `settings`
- **Token Validation**: Create separate `TokenData` models
- **Never**: Hardcode secrets, API keys, or passwords

## Error Handling Standards

### External Service Failures
```python
# Always return safe defaults for non-critical failures
try:
    result = await external_service_call()
    return result
except Exception as e:
    print(f"Service unavailable: {e}")
    return []  # or None, or default value
```

### Client Errors
```python
# Use HTTPException for client-facing errors
from fastapi import HTTPException, status

if not user_exists:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
```

## Configuration Management

- All settings in `app/core/config.py` using Pydantic Settings
- Environment variables with sensible defaults
- Import as: `from app.core.config import settings`
- Module-specific settings included in main Settings class

## Testing Requirements

For every new feature, create `tests/test_feature_name.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feature_success():
    # Test happy path
    pass

def test_feature_error_handling():
    # Test error scenarios
    pass
```

## Type Hints & Modern Python

- Use type hints for ALL function parameters and return values
- Use `list[Type]` and `dict[str, Type]` syntax (Python 3.9+)
- Use `Optional[Type]` for nullable fields
- Use `Union[Type1, Type2]` only when necessary