from fastapi import APIRouter, Depends
from typing import List
from . import schemas
from .service import deadline_service, DeadlineService

router = APIRouter(
    prefix="/deadline",
    tags=["deadline"],
)

@router.get("/jobs", response_model=List[schemas.DeadlineJob])
async def list_deadline_jobs(service: DeadlineService = Depends(lambda: deadline_service)):
    """
    Retrieve a list of jobs from Deadline.
    """
    return await service.get_jobs()
