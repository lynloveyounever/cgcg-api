from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_deadline_jobs():
    """
    Test the GET /deadline/jobs endpoint.
    """
    response = client.get("/deadline/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Check if the mock data structure is correct
    if len(response.json()) > 0:
        assert "id" in response.json()[0]
        assert "name" in response.json()[0]
        assert "status" in response.json()[0]
        assert "user" in response.json()[0]
