from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.api.v1.schemas.user_schemas import UserCreate

class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

def get_user_repository(db: Session):
    return UserRepository(db)
