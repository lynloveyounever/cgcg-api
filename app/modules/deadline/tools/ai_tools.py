"""
Deadline AI Tools API endpoints following function-calling specifications.
These endpoints are designed for AI agents with clear function names,
simple parameters, and structured responses.
Enhanced with MCP decorators for proper tool, resource, and prompt support.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
from ..service import deadline_service
from ..schemas import DeadlineRead

tools_router = APIRouter(tags=["Deadline AI Tools"])

# Create MCP instance for decorators
mcp = FastMCP("deadline-tools")


# Function-calling compatible models
class DeadlineJobInfo(BaseModel):
    """Simplified job information for AI function calls."""
    id: str = Field(description="Unique job identifier")
    name: str = Field(description="Job name or title")
    status: str = Field(description="Current job status (Completed, Rendering, Failed, etc.)")
    user: str = Field(description="User who submitted the job")


class JobStatusResult(BaseModel):
    """Job status check result for AI function calls."""
    job_id: str = Field(description="Job identifier")
    status: str = Field(description="Current status")
    is_running: bool = Field(description="Whether job is currently running")
    is_completed: bool = Field(description="Whether job is completed")
    needs_attention: bool = Field(description="Whether job needs human attention")


class WorkloadSummary(BaseModel):
    """Workload summary for AI analysis."""
    total_jobs: int = Field(description="Total number of jobs")
    running_jobs: int = Field(description="Number of currently running jobs")
    completed_jobs: int = Field(description="Number of completed jobs")
    failed_jobs: int = Field(description="Number of failed jobs")
    active_users: List[str] = Field(description="List of users with active jobs")


@mcp.tool()
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


@mcp.tool()
@tools_router.get("/get_jobs_by_status/{status}", response_model=List[DeadlineJobInfo])
async def get_jobs_by_status(status: str):
    """
    Get jobs filtered by status.
    
    Args:
        status: Job status to filter by (e.g., "Rendering", "Completed", "Failed")
    
    Returns a list of jobs matching the specified status.
    Use this to find jobs in a specific state.
    """
    jobs = await deadline_service.get_jobs()
    filtered_jobs = [job for job in jobs if job.status.lower() == status.lower()]
    
    return [
        DeadlineJobInfo(
            id=job.id,
            name=job.name,
            status=job.status,
            user=job.user
        )
        for job in filtered_jobs
    ]


@mcp.tool()
@tools_router.get("/get_jobs_by_user/{username}", response_model=List[DeadlineJobInfo])
async def get_jobs_by_user(username: str):
    """
    Get jobs for a specific user.
    
    Args:
        username: Username to filter jobs by
    
    Returns a list of jobs belonging to the specified user.
    Use this to see what jobs a particular user has submitted.
    """
    jobs = await deadline_service.get_jobs()
    user_jobs = [job for job in jobs if job.user.lower() == username.lower()]
    
    return [
        DeadlineJobInfo(
            id=job.id,
            name=job.name,
            status=job.status,
            user=job.user
        )
        for job in user_jobs
    ]


@mcp.tool()
@tools_router.get("/check_job_status/{job_id}", response_model=JobStatusResult)
async def check_job_status(job_id: str):
    """
    Check the status of a specific job.
    
    Args:
        job_id: The unique identifier of the job to check
    
    Returns detailed status information about the job.
    Use this to monitor individual job progress.
    """
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


@mcp.tool()
@tools_router.get("/get_workload_summary", response_model=WorkloadSummary)
async def get_workload_summary():
    """
    Get a summary of the current workload.
    
    Returns statistics about all jobs including counts by status
    and list of active users.
    Use this to understand the overall system workload.
    """
    jobs = await deadline_service.get_jobs()
    
    # Count jobs by status
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


@mcp.tool()
@tools_router.get("/get_failed_jobs", response_model=List[DeadlineJobInfo])
async def get_failed_jobs():
    """
    Get all jobs that have failed.
    
    Returns a list of jobs with failed or error status.
    Use this to identify jobs that need attention or troubleshooting.
    """
    jobs = await deadline_service.get_jobs()
    failed_jobs = [
        job for job in jobs 
        if job.status.lower() in ["failed", "error", "suspended"]
    ]
    
    return [
        DeadlineJobInfo(
            id=job.id,
            name=job.name,
            status=job.status,
            user=job.user
        )
        for job in failed_jobs
    ]


@mcp.tool()
@tools_router.get("/get_running_jobs", response_model=List[DeadlineJobInfo])
async def get_running_jobs():
    """
    Get all currently running jobs.
    
    Returns a list of jobs that are currently being processed.
    Use this to monitor active rendering or processing tasks.
    """
    jobs = await deadline_service.get_jobs()
    running_jobs = [
        job for job in jobs 
        if job.status.lower() in ["rendering", "queued", "processing"]
    ]
    
    return [
        DeadlineJobInfo(
            id=job.id,
            name=job.name,
            status=job.status,
            user=job.user
        )
        for job in running_jobs
    ]


@mcp.tool()
@tools_router.get("/count_jobs_by_status", response_model=Dict[str, int])
async def count_jobs_by_status():
    """
    Count jobs grouped by their status.
    
    Returns a dictionary with status names as keys and counts as values.
    Use this to get quick statistics about job distribution.
    """
    jobs = await deadline_service.get_jobs()
    status_counts = {}
    
    for job in jobs:
        status = job.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return status_counts


@mcp.tool()
@tools_router.get("/list_active_users", response_model=List[str])
async def list_active_users():
    """
    Get list of users who have jobs in the system.
    
    Returns a list of usernames who have submitted jobs.
    Use this to see which users are currently using the system.
    """
    jobs = await deadline_service.get_jobs()
    users = list(set(job.user for job in jobs))
    return sorted(users)


@mcp.tool()
@tools_router.get("/is_system_busy", response_model=Dict[str, Any])
async def is_system_busy():
    """
    Check if the render system is currently busy.
    
    Returns information about system load and whether it's busy.
    Use this to determine if it's a good time to submit new jobs.
    """
    jobs = await deadline_service.get_jobs()
    running_jobs = [
        job for job in jobs 
        if job.status.lower() in ["rendering", "queued", "processing"]
    ]
    
    total_jobs = len(jobs)
    running_count = len(running_jobs)
    
    # Consider system busy if more than 70% of jobs are running
    is_busy = running_count > (total_jobs * 0.7) if total_jobs > 0 else False
    
    return {
        "is_busy": is_busy,
        "total_jobs": total_jobs,
        "running_jobs": running_count,
        "load_percentage": round((running_count / total_jobs * 100) if total_jobs > 0 else 0, 1),
        "recommendation": "Wait for current jobs to complete" if is_busy else "System available for new jobs"
    }

# Example MCP Resources (read-only data access)
@mcp.resource("deadline://jobs")
async def jobs_resource() -> str:
    """
    Resource providing access to all deadline jobs data.
    
    This is a resource (not a tool) - it provides read-only access to data.
    Resources are for data that AI agents can read but not modify.
    """
    jobs = await deadline_service.get_jobs()
    return f"Total jobs: {len(jobs)}\nJobs: {[job.name for job in jobs]}"


@mcp.resource("deadline://config")
async def config_resource() -> str:
    """
    Resource providing access to deadline system configuration.
    
    Resources provide static or semi-static data that AI agents can reference.
    """
    return """
Deadline System Configuration:
- Max concurrent jobs: 10
- Default timeout: 30 minutes
- Supported formats: .blend, .ma, .max
- Render engines: Cycles, Arnold, V-Ray
"""


# Example MCP Prompts (text generation templates)
@mcp.prompt()
async def job_report_prompt(job_id: str) -> str:
    """
    Generate a detailed report for a specific job.
    
    This is a prompt (not a tool) - it generates human-readable text.
    Prompts are for generating reports, summaries, or formatted output.
    """
    jobs = await deadline_service.get_jobs()
    job = next((j for j in jobs if j.id == job_id), None)
    
    if not job:
        return f"Job {job_id} not found."
    
    return f"""
# Deadline Job Report

**Job ID**: {job.id}
**Name**: {job.name}
**Status**: {job.status}
**User**: {job.user}

## Summary
This job is currently {job.status.lower()}. 
{'✅ Job completed successfully.' if job.status == 'Completed' else '⏳ Job is still processing.' if job.status == 'Rendering' else '❌ Job needs attention.'}

## Recommendations
{'No action needed.' if job.status == 'Completed' else 'Monitor progress.' if job.status == 'Rendering' else 'Check logs and restart if necessary.'}
"""


@mcp.prompt()
async def system_status_prompt() -> str:
    """
    Generate a human-readable system status report.
    
    Prompts generate formatted text for human consumption.
    """
    jobs = await deadline_service.get_jobs()
    
    running_jobs = [job for job in jobs if job.status.lower() in ["rendering", "queued", "processing"]]
    completed_jobs = [job for job in jobs if job.status.lower() == "completed"]
    failed_jobs = [job for job in jobs if job.status.lower() in ["failed", "error"]]
    
    return f"""
# 🎬 Deadline System Status Report

## 📊 Overview
- **Total Jobs**: {len(jobs)}
- **Running**: {len(running_jobs)} 🟢
- **Completed**: {len(completed_jobs)} ✅
- **Failed**: {len(failed_jobs)} ❌

## 🔄 Active Jobs
{chr(10).join([f"- {job.name} ({job.user})" for job in running_jobs[:5]]) if running_jobs else "No active jobs"}

## ⚠️ Issues
{chr(10).join([f"- {job.name} - {job.status}" for job in failed_jobs]) if failed_jobs else "No issues detected"}

## 💡 System Health
{'🟢 System running smoothly' if len(failed_jobs) == 0 else '🟡 Some jobs need attention' if len(failed_jobs) < 3 else '🔴 Multiple issues detected'}
"""