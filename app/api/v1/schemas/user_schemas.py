# Pydantic schemas for User API requests and responses
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
