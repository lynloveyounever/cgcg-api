# app/api/endpoints/jobs.py

from fastapi import APIRouter, HTTPException, Depends
# from deadline import service
from typing import Optional
from pydantic import BaseModel
import enum

router = APIRouter(prefix="/deadline", tags=["Applications"])

class JobStatus(enum.Enum):
    """
    Represents the possible statuses of a job.
    """
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SUSPEND = "suspend"

class Job(BaseModel):
    job_id: str
    job_name: Optional[str] = None
    status: JobStatus # Use the Enum as the type hint

class Response(BaseModel):
    status: str
    message: str
    data: Optional[dict] = {'lalala': 'ttata'}

def launch_deadline_service():
    return 'service()'


    
@router.get("/jobs/{job_id}", response_model=Response)
def get_job(job: Job, deadline_service: str = Depends(launch_deadline_service)):

    return Response

@router.get("/{locate}/jobs/{job_id}")
def get_specific_job(locate: str, job_id: str, deadline_service: str = Depends(launch_deadline_service)):
    job_info = deadline_service.get_job_by_id(job_id)
    if job_info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_info

@router.get("/{locate}/{status}")
def read_status_jobs(locate: str, status: str, deadline_service: str = Depends(launch_deadline_service)):
    job_info = deadline_service.get_job_by_status(status)

@router.get("/jobs")
def read_jobs():
    return {"message": "This endpoint will return Deadline jobs."}


