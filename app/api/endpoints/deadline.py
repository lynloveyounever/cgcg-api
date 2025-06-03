# app/api/endpoints/jobs.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.deadline import service

router = APIRouter(prefix="/deadline", tags=["Applications"])


def get_job_service():
    return service()
    
@router.get("/jobs/{job_id}")
def read_job(job_id: str, deadline_service: service = Depends(get_job_service)):
    job_info = deadline_service.get_job_by_id(job_id)
    if job_info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_info

@router.get("/jobs")
def read_jobs():
    return {"message": "This endpoint will return Deadline jobs."}


