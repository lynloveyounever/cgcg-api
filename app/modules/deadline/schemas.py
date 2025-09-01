# Pydantic models for Deadline data
from pydantic import BaseModel

class DeadlineJob(BaseModel):
    id: str
    name: str
    status: str
    user: str
