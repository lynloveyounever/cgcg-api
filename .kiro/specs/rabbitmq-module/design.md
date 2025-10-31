# RabbitMQ Module Design Document

## Overview

The RabbitMQ integration provides a configurable messaging solution for the CGCG API, supporting both high-level Celery task queues and low-level direct RabbitMQ messaging. The implementation uses dependency injection to allow RabbitMQ to be enabled/disabled via configuration, making it optional infrastructure that other services can depend on when available.

## Architecture

### Hybrid Messaging Approach

The module implements two complementary messaging patterns:

1. **Celery Task Queues**: High-level distributed task processing with automatic retry, result storage, and worker management
2. **Direct RabbitMQ Messaging**: Low-level message publishing and queue management for custom messaging patterns

### Flexible Architecture Structure

**Core Infrastructure** (always available):
```
app/core/
├── config.py               # RabbitMQ configuration flags
└── dependencies.py         # Dependency injection for messaging

app/services/
├── messaging_service.py    # Abstract messaging interface
└── rabbitmq_service.py     # RabbitMQ implementation (optional)
```

**Optional Management Module** (when enabled):
```
app/modules/rabbitmq/
├── __init__.py             # Module initialization
├── router.py               # Management endpoints
├── schemas.py              # Request/response models
└── admin_service.py        # Queue management operations
```

**Configuration-Driven Loading**:
- `RABBITMQ_ENABLED: bool = False` - Enable/disable RabbitMQ
- `RABBITMQ_MANAGEMENT_ENABLED: bool = False` - Enable management endpoints
- Graceful fallback when RabbitMQ is unavailable

## Components and Interfaces

### 1. Configuration (app/core/config.py)

Extended Settings class with configurable RabbitMQ:

```python
class Settings(BaseSettings):
    # Existing settings...
    
    # RabbitMQ Feature Flags
    RABBITMQ_ENABLED: bool = False
    RABBITMQ_MANAGEMENT_ENABLED: bool = False
    
    # RabbitMQ Configuration (only used when enabled)
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USERNAME: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "rpc://"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    
    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.RABBITMQ_USERNAME}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
```

### 2. Dependency Injection (app/core/dependencies.py)

Configurable messaging dependencies:

```python
from typing import Optional
from app.core.config import settings
from app.services.messaging_service import MessagingService, NoOpMessagingService
from app.services.rabbitmq_service import RabbitMQService

async def get_messaging_service() -> MessagingService:
    """Returns messaging service based on configuration"""
    if settings.RABBITMQ_ENABLED:
        try:
            return RabbitMQService(settings)
        except Exception:
            # Fallback to no-op service if RabbitMQ unavailable
            return NoOpMessagingService()
    return NoOpMessagingService()

# Usage in other services:
# messaging: MessagingService = Depends(get_messaging_service)
```

### 3. Abstract Messaging Interface (app/services/messaging_service.py)

Base interface for messaging operations:

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class MessagingService(ABC):
    @abstractmethod
    async def publish_message(self, queue: str, message: dict) -> Optional[str]:
        """Publish message to queue, returns message ID or None if disabled"""
        pass
    
    @abstractmethod
    async def submit_task(self, task_name: str, *args, **kwargs) -> Optional[str]:
        """Submit async task, returns task ID or None if disabled"""
        pass

class NoOpMessagingService(MessagingService):
    """No-operation implementation when messaging is disabled"""
    async def publish_message(self, queue: str, message: dict) -> None:
        return None
    
    async def submit_task(self, task_name: str, *args, **kwargs) -> None:
        return None
```

### 4. Connection Manager (app/services/rabbitmq_service.py)

Manages RabbitMQ connections and channels:

```python
class RabbitMQConnection:
    def __init__(self, settings: Settings)
    async def get_connection() -> aio_pika.Connection
    async def get_channel() -> aio_pika.Channel
    async def close_connection()
    
class ConnectionManager:
    def __init__(self, settings: Settings)
    async def __aenter__() -> aio_pika.Channel
    async def __aexit__()
```

### 3. Celery Application (celery_app.py)

Celery configuration and application setup:

```python
def create_celery_app(settings: Settings) -> Celery
def get_celery_app() -> Celery

# Task registration and discovery
@celery_app.task
def sample_task(data: dict) -> dict
```

### 4. Service Layer (service.py)

Core business logic for messaging operations:

```python
class RabbitMQService:
    def __init__(self, settings: Settings)
    
    # Celery operations
    async def submit_task(task_name: str, args: list, kwargs: dict) -> str
    async def get_task_status(task_id: str) -> dict
    async def revoke_task(task_id: str) -> bool
    async def list_active_tasks() -> list
    
    # Direct messaging operations
    async def publish_message(queue_name: str, message: dict, routing_key: str = None) -> str
    async def declare_queue(queue_name: str, durable: bool = True, **kwargs) -> bool
    async def get_queue_info(queue_name: str) -> dict
    async def purge_queue(queue_name: str) -> int
```

### 5. Schemas (schemas.py)

Pydantic models for request/response validation:

```python
# Task-related schemas
class TaskSubmissionRequest(BaseModel):
    task_name: str
    args: list = []
    kwargs: dict = {}

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None

# Direct messaging schemas
class MessagePublishRequest(BaseModel):
    queue_name: str
    message: dict
    routing_key: Optional[str] = None
    exchange: Optional[str] = None

class QueueDeclarationRequest(BaseModel):
    queue_name: str
    durable: bool = True
    exclusive: bool = False
    auto_delete: bool = False

class QueueInfoResponse(BaseModel):
    queue_name: str
    message_count: int
    consumer_count: int
    durable: bool
```

### 6. Router (router.py)

FastAPI endpoints for RabbitMQ operations:

```python
router = APIRouter(prefix="/rabbitmq", tags=["RabbitMQ"])

# Celery endpoints
@router.post("/tasks/submit", response_model=TaskStatusResponse)
@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
@router.delete("/tasks/{task_id}")
@router.get("/tasks/active", response_model=List[TaskStatusResponse])

# Direct messaging endpoints
@router.post("/messages/publish")
@router.post("/queues/declare")
@router.get("/queues/{queue_name}/info", response_model=QueueInfoResponse)
@router.delete("/queues/{queue_name}/purge")
```

## Data Models

### Task Execution Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Celery
    participant RabbitMQ
    participant Worker

    Client->>API: POST /rabbitmq/tasks/submit
    API->>Celery: submit_task()
    Celery->>RabbitMQ: Queue task message
    RabbitMQ->>Worker: Deliver task
    Worker->>RabbitMQ: Store result
    API->>Client: Return task_id
    
    Client->>API: GET /rabbitmq/tasks/{task_id}
    API->>Celery: get_task_status()
    Celery->>API: Task status & result
    API->>Client: Return status
```

### Direct Messaging Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant RabbitMQ

    Client->>API: POST /rabbitmq/messages/publish
    API->>RabbitMQ: Publish message to queue
    RabbitMQ->>API: Confirm delivery
    API->>Client: Return message_id
    
    Client->>API: GET /rabbitmq/queues/{name}/info
    API->>RabbitMQ: Query queue statistics
    RabbitMQ->>API: Queue info
    API->>Client: Return queue details
```

## Error Handling

### Connection Management
- Automatic connection retry with exponential backoff
- Connection pooling for high-throughput scenarios
- Graceful degradation when RabbitMQ is unavailable

### Task Management
- Task timeout handling with configurable limits
- Dead letter queue for failed tasks
- Task result expiration and cleanup

### API Error Responses
- Standardized error format following existing API patterns
- Specific error codes for different failure scenarios
- Detailed error messages for debugging

### Error Categories

```python
class RabbitMQError(Exception):
    """Base exception for RabbitMQ operations"""

class ConnectionError(RabbitMQError):
    """RabbitMQ connection failures"""

class TaskError(RabbitMQError):
    """Celery task execution errors"""

class QueueError(RabbitMQError):
    """Queue management errors"""
```

## Testing Strategy

### Unit Tests
- Service layer methods with mocked RabbitMQ connections
- Schema validation for all request/response models
- Configuration validation and default value testing
- Error handling scenarios

### Integration Tests
- End-to-end task submission and execution
- Direct message publishing and queue management
- Connection failure and recovery scenarios
- Multiple worker coordination

### Test Structure
```
tests/
├── test_rabbitmq_service.py      # Service layer tests
├── test_rabbitmq_router.py       # API endpoint tests
├── test_rabbitmq_connection.py   # Connection management tests
├── test_celery_integration.py    # Celery-specific tests
└── conftest.py                   # Test fixtures and setup
```

### Test Dependencies
- `pytest-asyncio` for async test support
- `pytest-mock` for mocking RabbitMQ connections
- `celery[pytest]` for Celery testing utilities
- Test RabbitMQ instance or containerized testing environment

## Dependencies

### Required Packages
```
celery[redis]==5.3.4          # Task queue framework
aio-pika==9.3.1               # Async RabbitMQ client
pika==1.3.2                   # Sync RabbitMQ client (fallback)
kombu==5.3.4                  # Messaging library (Celery dependency)
```

### Optional Packages
```
flower==2.0.1                 # Celery monitoring (development)
redis==5.0.1                  # Alternative result backend
```

## Performance Considerations

### Connection Pooling
- Reuse connections across requests
- Configure appropriate pool sizes based on load
- Monitor connection health and automatic cleanup

### Message Serialization
- JSON serialization for compatibility
- Optional binary serialization for performance-critical tasks
- Message compression for large payloads

### Scalability
- Horizontal scaling through multiple Celery workers
- Queue partitioning for high-throughput scenarios
- Load balancing across RabbitMQ cluster nodes

## Security Considerations

### Authentication
- Secure credential management through environment variables
- Support for RabbitMQ user permissions and virtual hosts
- SSL/TLS connection support for production deployments

### Message Security
- Input validation for all message payloads
- Rate limiting for API endpoints
- Message encryption for sensitive data (optional)

### Access Control
- Role-based access to different queue operations
- API key authentication for external integrations
- Audit logging for message operations