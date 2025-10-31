# FastMCP Decorator Approach Analysis

## Current vs Decorated Approach

### Current (HTTP Only)
```python
@tools_router.get("/get_all_jobs", response_model=List[DeadlineJobInfo])
async def get_all_jobs():
    """Get all deadline jobs."""
    jobs = await deadline_service.get_jobs()
    return [DeadlineJobInfo(...) for job in jobs]
```

### With FastMCP Decorators (HTTP + MCP)
```python
from fastapi_mcp import mcp_tool

@mcp_tool(name="get_all_deadline_jobs", description="Get all deadline jobs in the system")
@tools_router.get("/get_all_jobs", response_model=List[DeadlineJobInfo])
async def get_all_jobs():
    """Get all deadline jobs."""
    jobs = await deadline_service.get_jobs()
    return [DeadlineJobInfo(...) for job in jobs]
```

## Benefits of Decorator Approach

### ✅ **Dual Protocol Support**
- Same function serves both HTTP and MCP protocols
- No code duplication
- Consistent behavior across protocols

### ✅ **Clean Architecture**
- Functions remain in their logical modules
- No coupling between MCP and business logic
- Decorators are just metadata

### ✅ **Auto-Discovery**
- FastMCP automatically discovers decorated functions
- No manual registration needed
- Functions appear in MCP tool list automatically

### ✅ **Maintainability**
- Add/remove MCP support with just a decorator
- Function logic stays the same
- Easy to enable/disable MCP per function

## Implementation Example

```python
# app/modules/deadline/tools/ai_tools.py
from fastapi import APIRouter, HTTPException
from fastapi_mcp import mcp_tool
from typing import List, Dict, Any
from ..service import deadline_service
from ..schemas import DeadlineRead

tools_router = APIRouter(tags=["Deadline AI Tools"])

@mcp_tool(
    name="get_all_deadline_jobs",
    description="Get all deadline jobs in the system with basic information"
)
@tools_router.get("/get_all_jobs", response_model=List[DeadlineJobInfo])
async def get_all_jobs():
    """
    Get all deadline jobs.
    
    Returns a list of all jobs in the system with basic information.
    Use this function to get an overview of all current jobs.
    """
    jobs = await deadline_service.get_jobs()
    return [
        DeadlineJobInfo(
            id=job.id,
            name=job.name,
            status=job.status,
            user=job.user
        )
        for job in jobs
    ]

@mcp_tool(
    name="check_deadline_job_status",
    description="Check the status of a specific deadline job by ID"
)
@tools_router.get("/check_job_status/{job_id}", response_model=JobStatusResult)
async def check_job_status(job_id: str):
    """Check specific job status with AI-friendly response format."""
    jobs = await deadline_service.get_jobs()
    job = next((j for j in jobs if j.id == job_id), None)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    status_lower = job.status.lower()
    
    return JobStatusResult(
        job_id=job.id,
        status=job.status,
        is_running=status_lower in ["rendering", "queued", "processing"],
        is_completed=status_lower == "completed",
        needs_attention=status_lower in ["failed", "error", "suspended"]
    )

@mcp_tool(
    name="get_deadline_workload_summary",
    description="Get summary of current deadline workload including job counts and active users"
)
@tools_router.get("/get_workload_summary", response_model=WorkloadSummary)
async def get_workload_summary():
    """Get a summary of the current workload."""
    jobs = await deadline_service.get_jobs()
    
    # Calculate statistics
    running_count = 0
    completed_count = 0
    failed_count = 0
    active_users = set()
    
    for job in jobs:
        status_lower = job.status.lower()
        if status_lower in ["rendering", "queued", "processing"]:
            running_count += 1
            active_users.add(job.user)
        elif status_lower == "completed":
            completed_count += 1
        elif status_lower in ["failed", "error"]:
            failed_count += 1
    
    return WorkloadSummary(
        total_jobs=len(jobs),
        running_jobs=running_count,
        completed_jobs=completed_count,
        failed_jobs=failed_count,
        active_users=list(active_users)
    )
```

## Result

### HTTP Access (Testing & Direct Integration)
```bash
GET /api/v1/deadline/tools/get_all_jobs
GET /api/v1/deadline/tools/check_job_status/job-001
GET /api/v1/deadline/tools/get_workload_summary
```

### MCP Access (AI Agents)
```json
{
  "tools": [
    {
      "name": "get_all_deadline_jobs",
      "description": "Get all deadline jobs in the system with basic information"
    },
    {
      "name": "check_deadline_job_status", 
      "description": "Check the status of a specific deadline job by ID"
    },
    {
      "name": "get_deadline_workload_summary",
      "description": "Get summary of current deadline workload including job counts and active users"
    }
  ]
}
```

## Best Practices for MCP Decorators

### 1. **Clear Tool Names**
```python
@mcp_tool(name="get_all_deadline_jobs")  # Prefixed with module
```

### 2. **Descriptive Descriptions**
```python
@mcp_tool(description="Get all deadline jobs in the system with basic information")
```

### 3. **Consistent Naming Convention**
```python
# Pattern: {action}_{module}_{resource}
get_all_deadline_jobs
check_deadline_job_status
get_deadline_workload_summary
```

### 4. **Parameter Documentation**
```python
@mcp_tool(
    name="get_jobs_by_status",
    description="Get deadline jobs filtered by status",
    parameters={
        "status": "Job status to filter by (Rendering, Completed, Failed)"
    }
)
```

## Recommendation: YES, Add Decorators!

### Why This Approach is Excellent:

1. **Zero Architectural Changes** - Functions stay where they are
2. **Dual Protocol Support** - HTTP + MCP from same functions  
3. **Easy to Implement** - Just add decorators
4. **Easy to Remove** - Remove decorators if needed
5. **Auto-Discovery** - MCP finds tools automatically
6. **Clean Separation** - Business logic unchanged

### Implementation Steps:

1. Add FastMCP decorators to existing functions
2. Keep current HTTP endpoints unchanged
3. MCP automatically discovers and exposes tools
4. Test both HTTP and MCP access

This gives you the best of both worlds with minimal changes!