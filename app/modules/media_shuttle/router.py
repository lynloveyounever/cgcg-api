

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from . import schemas
from .service import media_shuttle_service, MediaShuttleService

router = APIRouter(
    tags=["Media Shuttle"],
    prefix="/media_shuttle"
)

@router.post("/transfers", response_model=schemas.Transfer, status_code=201)
def create_transfer(transfer: schemas.TransferCreate, service: MediaShuttleService = Depends(lambda: media_shuttle_service)):
    """Create a new transfer job."""
    return service.create_transfer(transfer)

@router.get("/transfers", response_model=List[schemas.Transfer])
def list_transfers(service: MediaShuttleService = Depends(lambda: media_shuttle_service)):
    """List all transfer jobs."""
    return service.get_all_transfers()

@router.get("/transfers/{transfer_id}", response_model=schemas.Transfer)
def get_transfer(transfer_id: int, service: MediaShuttleService = Depends(lambda: media_shuttle_service)):
    """Get a specific transfer job by its ID."""
    db_transfer = service.get_transfer_by_id(transfer_id)
    if db_transfer is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return db_transfer

@router.put("/transfers/{transfer_id}", response_model=schemas.Transfer)
def update_transfer(transfer_id: int, transfer: schemas.TransferUpdate, service: MediaShuttleService = Depends(lambda: media_shuttle_service)):
    """Update a transfer job."""
    updated_transfer = service.update_transfer(transfer_id, transfer)
    if updated_transfer is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return updated_transfer

@router.delete("/transfers/{transfer_id}", response_model=schemas.Transfer)
def delete_transfer(transfer_id: int, service: MediaShuttleService = Depends(lambda: media_shuttle_service)):
    """Delete a transfer job."""
    deleted_transfer = service.delete_transfer(transfer_id)
    if deleted_transfer is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return deleted_transfer