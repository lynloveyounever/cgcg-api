from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field


class JobStatus(str, Enum):
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

class UserBase(BaseModel):
    locate: str = Field(min_length=1, max_length=128)
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9_-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=1)

    

class Response(BaseModel):
    status: str
    message: str
    data: Optional[dict] = {'lalala': 'ttata'}
