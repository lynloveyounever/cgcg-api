from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """
    Test the root endpoint to ensure it returns a 200 OK status
    and the correct welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CGCG API. All endpoints are available under /api/v1"}
