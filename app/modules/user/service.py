# Business logic for user management
from typing import List, Dict, Optional
from . import schemas

# In-memory database for demonstration
fake_user_db: Dict[int, schemas.User] = {
    1: schemas.User(id=1, username="lynloveyounever", email="lynloveyounever@example.com", full_name="Lyn Loveyounever"),
    2: schemas.User(id=2, username="testuser", email="test@example.com", full_name="Test User"),
}

class UserService:
    def get_all_users(self) -> List[schemas.User]:
        """Retrieves all users from the database."""
        return list(fake_user_db.values())

    def get_user_by_id(self, user_id: int) -> Optional[schemas.User]:
        """Retrieves a single user by their ID."""
        return fake_user_db.get(user_id)

    def create_user(self, user: schemas.UserCreate) -> schemas.User:
        """Creates a new user and adds them to the database."""
        new_id = max(fake_user_db.keys()) + 1 if fake_user_db else 1
        new_user = schemas.User(id=new_id, **user.model_dump())
        fake_user_db[new_id] = new_user
        return new_user

    def update_user(self, user_id: int, user_update: schemas.UserUpdate) -> Optional[schemas.User]:
        """Updates an existing user's information."""
        if user_id not in fake_user_db:
            return None
        stored_user = fake_user_db[user_id]
        update_data = user_update.model_dump(exclude_unset=True)
        updated_user = stored_user.model_copy(update=update_data)
        fake_user_db[user_id] = updated_user
        return updated_user

    def delete_user(self, user_id: int) -> Optional[schemas.User]:
        """Deletes a user from the database."""
        if user_id not in fake_user_db:
            return None
        return fake_user_db.pop(user_id)

# Create a single, importable instance of the service
user_service = UserService()
