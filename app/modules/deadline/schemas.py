# Pydantic models for Deadline data
from typing import Optional
from pydantic import BaseModel

class DeadlineJob(BaseModel):
    id: str
    name: str
    status: str
    user: str
    region: Optional[str] = None  # Add region context
    priority: Optional[int] = None
    progress: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# Alias for compatibility
DeadlineRead = DeadlineJob