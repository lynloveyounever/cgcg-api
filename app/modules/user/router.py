# API endpoints for user management
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from . import schemas
from .service import user_service, UserService

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@router.post("/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, service: UserService = Depends(lambda: user_service)):
    """Create a new user."""
    # In a real app, you'd check if the user already exists
    return service.create_user(user)

@router.get("/", response_model=List[schemas.User])
def list_users(service: UserService = Depends(lambda: user_service)):
    """List all users."""
    return service.get_all_users()

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, service: UserService = Depends(lambda: user_service)):
    """Get a specific user by their ID."""
    db_user = service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, service: UserService = Depends(lambda: user_service)):
    """Update a user's information."""
    updated_user = service.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, service: UserService = Depends(lambda: user_service)):
    """Delete a user."""
    deleted_user = service.delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
