# Pydantic models for Media Shuttle data
from pydantic import BaseModel
from typing import Optional

class TransferBase(BaseModel):
    source_path: str
    destination_path: str
    status: str = "pending"

class TransferCreate(TransferBase):
    pass

class TransferUpdate(BaseModel):
    source_path: Optional[str] = None
    destination_path: Optional[str] = None
    status: Optional[str] = None

class Transfer(TransferBase):
    id: int

    class Config:
        from_attributes = True
