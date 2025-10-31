# Function-Calling API Specification

This document describes the AI Tools API endpoints designed for function-calling compatibility with AI agents and language models.

## Function-Calling Design Principles

1. **Clear Function Names**: Use descriptive, action-oriented names (e.g., `get_all_jobs`, `check_job_status`)
2. **Simple Parameters**: Minimal, well-typed parameters with clear descriptions
3. **Structured Responses**: Consistent, predictable response formats
4. **Single Responsibility**: Each function does one thing well
5. **Error Handling**: Clear error messages and status codes

## Available Functions

### Job Retrieval Functions

#### `get_all_jobs()`
**Purpose**: Get all deadline jobs in the system
**Parameters**: None
**Returns**: List of job objects with id, name, status, user
**Use Case**: Get overview of all current jobs

```json
[
  {
    "id": "job-001",
    "name": "Scene_01_Render",
    "status": "Completed",
    "user": "lynloveyounever"
  }
]
```

#### `get_jobs_by_status(status: str)`
**Purpose**: Get jobs filtered by specific status
**Parameters**: 
- `status`: Job status to filter by (e.g., "Rendering", "Completed", "Failed")
**Returns**: List of matching jobs
**Use Case**: Find jobs in a specific state

#### `get_jobs_by_user(username: str)`
**Purpose**: Get jobs for a specific user
**Parameters**:
- `username`: Username to filter jobs by
**Returns**: List of user's jobs
**Use Case**: See what jobs a particular user has submitted

#### `get_failed_jobs()`
**Purpose**: Get all jobs that have failed
**Parameters**: None
**Returns**: List of failed jobs
**Use Case**: Identify jobs that need attention

#### `get_running_jobs()`
**Purpose**: Get all currently running jobs
**Parameters**: None
**Returns**: List of active jobs
**Use Case**: Monitor active rendering tasks

### Status Check Functions

#### `check_job_status(job_id: str)`
**Purpose**: Check the status of a specific job
**Parameters**:
- `job_id`: Unique identifier of the job
**Returns**: Detailed status information
**Use Case**: Monitor individual job progress

```json
{
  "job_id": "job-001",
  "status": "Completed",
  "is_running": false,
  "is_completed": true,
  "needs_attention": false
}
```

#### `is_system_busy()`
**Purpose**: Check if the render system is currently busy
**Parameters**: None
**Returns**: System load information and recommendations
**Use Case**: Determine if it's a good time to submit new jobs

```json
{
  "is_busy": false,
  "total_jobs": 5,
  "running_jobs": 1,
  "load_percentage": 20.0,
  "recommendation": "System available for new jobs"
}
```

### Summary Functions

#### `get_workload_summary()`
**Purpose**: Get summary of current workload
**Parameters**: None
**Returns**: Statistics about all jobs
**Use Case**: Understand overall system workload

```json
{
  "total_jobs": 5,
  "running_jobs": 1,
  "completed_jobs": 3,
  "failed_jobs": 1,
  "active_users": ["lynloveyounever"]
}
```

#### `count_jobs_by_status()`
**Purpose**: Count jobs grouped by status
**Parameters**: None
**Returns**: Dictionary with status counts
**Use Case**: Get quick statistics about job distribution

```json
{
  "Completed": 3,
  "Rendering": 1,
  "Failed": 1
}
```

#### `list_active_users()`
**Purpose**: Get list of users with jobs in the system
**Parameters**: None
**Returns**: List of usernames
**Use Case**: See which users are currently using the system

```json
["lynloveyounever", "artist2", "animator1"]
```

## Function-Calling Examples

### OpenAI Function Calling Format

```json
{
  "name": "get_jobs_by_status",
  "description": "Get jobs filtered by status",
  "parameters": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "description": "Job status to filter by (e.g., 'Rendering', 'Completed', 'Failed')"
      }
    },
    "required": ["status"]
  }
}
```

### Usage in AI Agent Code

```python
# Check if system is busy before submitting new jobs
system_status = await call_function("is_system_busy")
if not system_status["is_busy"]:
    print("System available for new jobs")
else:
    print(f"System busy: {system_status['recommendation']}")

# Get failed jobs that need attention
failed_jobs = await call_function("get_failed_jobs")
if failed_jobs:
    print(f"Found {len(failed_jobs)} failed jobs that need attention")
    for job in failed_jobs:
        print(f"- {job['name']} (ID: {job['id']})")

# Monitor specific job progress
job_status = await call_function("check_job_status", {"job_id": "job-001"})
if job_status["needs_attention"]:
    print(f"Job {job_status['job_id']} needs attention: {job_status['status']}")
```

### Anthropic Claude Function Calling

```xml
<function_calls>
<invoke name="get_workload_summary">
</invoke>
</function_calls>

<function_calls>
<invoke name="get_jobs_by_status">
<parameter name="status">Failed</parameter>
</invoke>
</function_calls>
```

## Response Format Standards

All function responses follow these standards:

1. **Consistent Structure**: Same fields always present
2. **Clear Types**: Strings, numbers, booleans, arrays, objects
3. **Descriptive Fields**: Field names clearly indicate their purpose
4. **No Nested Complexity**: Flat structures when possible
5. **Error Handling**: HTTP status codes + error messages

## Error Responses

```json
{
  "detail": "Job job-999 not found"
}
```

## Integration with AI Frameworks

### LangChain Tool Integration

```python
from langchain.tools import BaseTool

class DeadlineJobsTool(BaseTool):
    name = "get_all_jobs"
    description = "Get all deadline jobs in the system"
    
    def _run(self, **kwargs):
        response = requests.get("/api/v1/deadline/tools/get_all_jobs")
        return response.json()
```

### OpenAI Assistant Integration

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_job_status",
            "description": "Check the status of a specific deadline job",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The unique identifier of the job to check"
                    }
                },
                "required": ["job_id"]
            }
        }
    }
]
```

This function-calling API design ensures AI agents can easily discover, understand, and use the deadline management capabilities effectively.