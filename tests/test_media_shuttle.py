from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_transfers():
    """Test listing all transfers."""
    response = client.get("/media_shuttle/transfers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2 # Based on fake_db

def test_create_and_get_transfer():
    """Test creating a new transfer and then retrieving it."""
    new_transfer_data = {
        "source_path": "/test/source.mov",
        "destination_path": "/test/dest.mov"
    }
    # Create
    response_create = client.post("/media_shuttle/transfers", json=new_transfer_data)
    assert response_create.status_code == 201
    created_transfer = response_create.json()
    assert created_transfer["source_path"] == new_transfer_data["source_path"]
    assert "id" in created_transfer
    new_id = created_transfer["id"]

    # Get
    response_get = client.get(f"/media_shuttle/transfers/{new_id}")
    assert response_get.status_code == 200
    assert response_get.json() == created_transfer

    # Cleanup (delete the created transfer)
    response_delete = client.delete(f"/media_shuttle/transfers/{new_id}")
    assert response_delete.status_code == 200
