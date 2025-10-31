"""
Deadline REST API endpoints for human users.
These endpoints provide standard CRUD operations and user-friendly responses.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..service import deadline_service
from ..schemas import DeadlineRead

rest_router = APIRouter(tags=["Deadline REST API"])


@rest_router.get("/jobs", response_model=List[DeadlineRead])
async def get_deadline_jobs(
    status: Optional[str] = Query(None, description="Filter by job status"),
    user: Optional[str] = Query(None, description="Filter by user"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of jobs to return")
):
    """
    Get deadline jobs with optional filtering.
    
    This endpoint is designed for human users and web interfaces.
    Provides pagination and filtering capabilities.
    """
    jobs = await deadline_service.get_jobs()
    
    # Apply filters
    if status:
        jobs = [job for job in jobs if job.status.lower() == status.lower()]
    
    if user:
        jobs = [job for job in jobs if job.user.lower() == user.lower()]
    
    # Apply limit
    return jobs[:limit]


@rest_router.get("/jobs/{job_id}", response_model=DeadlineRead)
async def get_deadline_job(job_id: str):
    """
    Get a specific deadline job by ID.
    
    Returns detailed information about a single job.
    """
    jobs = await deadline_service.get_jobs()
    job = next((j for j in jobs if j.id == job_id), None)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return job


@rest_router.get("/users", response_model=List[str])
async def get_deadline_users():
    """
    Get list of all users who have deadline jobs.
    
    Useful for filtering and user management interfaces.
    """
    jobs = await deadline_service.get_jobs()
    users = list(set(job.user for job in jobs))
    return sorted(users)


@rest_router.get("/status")
async def get_deadline_status():
    """
    Get deadline service status and statistics.
    
    Provides service health information and job statistics.
    """
    jobs = await deadline_service.get_jobs()
    
    # Calculate statistics
    total_jobs = len(jobs)
    status_counts = {}
    user_counts = {}
    
    for job in jobs:
        status_counts[job.status] = status_counts.get(job.status, 0) + 1
        user_counts[job.user] = user_counts.get(job.user, 0) + 1
    
    return {
        "service_available": True,
        "message": "Deadline service is running",
        "statistics": {
            "total_jobs": total_jobs,
            "status_breakdown": status_counts,
            "user_breakdown": user_counts,
            "active_users": len(user_counts)
        }
    }
