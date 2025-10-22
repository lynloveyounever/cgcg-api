from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_users():
    """Test listing all users."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2  # Based on the initial fake_user_db

def test_create_and_get_user():
    """Test creating a new user and then retrieving, updating, and deleting it."""
    new_user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "full_name": "New User"
    }
    
    # 1. Create User
    response_create = client.post("/api/v1/users/", json=new_user_data)
    assert response_create.status_code == 201
    created_user = response_create.json()
    assert created_user["username"] == new_user_data["username"]
    assert "id" in created_user
    new_id = created_user["id"]

    # 2. Get User
    response_get = client.get(f"/api/v1/users/{new_id}")
    assert response_get.status_code == 200
    assert response_get.json() == created_user

    # 3. Update User
    update_data = {"full_name": "A Brand New User Name"}
    response_update = client.put(f"/api/v1/users/{new_id}", json=update_data)
    assert response_update.status_code == 200
    updated_user = response_update.json()
    assert updated_user["full_name"] == "A Brand New User Name"
    assert updated_user["username"] == new_user_data["username"] # Ensure other fields are unchanged

    # 4. Delete User
    response_delete = client.delete(f"/api/v1/users/{new_id}")
    assert response_delete.status_code == 200
    assert response_delete.json() == updated_user # FastAPI returns the deleted object

    # 5. Verify Deletion
    response_get_deleted = client.get(f"/api/v1/users/{new_id}")
    assert response_get_deleted.status_code == 404


def test_read_current_user():
    """Test reading the current user."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json() == {"username": "fakecurrentuser"}
