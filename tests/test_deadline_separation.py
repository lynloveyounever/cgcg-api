"""
Tests for deadline module REST vs Tools API separation.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_deadline_rest_api_jobs():
    """Test REST API endpoint for human users."""
    response = client.get("/api/v1/deadline/rest/jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deadline_rest_api_status():
    """Test REST API status endpoint with statistics."""
    response = client.get("/api/v1/deadline/rest/status")
    assert response.status_code == 200
    data = response.json()
    assert "service_available" in data
    assert "statistics" in data
    assert "total_jobs" in data["statistics"]


def test_deadline_rest_api_users():
    """Test REST API users endpoint."""
    response = client.get("/api/v1/deadline/rest/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deadline_rest_api_single_job():
    """Test REST API single job endpoint."""
    # First get all jobs to find a valid ID
    response = client.get("/api/v1/deadline/rest/jobs")
    jobs = response.json()
    
    if jobs:
        job_id = jobs[0]["id"]
        response = client.get(f"/api/v1/deadline/rest/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id


def test_deadline_tools_get_all_jobs():
    """Test AI Tools API get all jobs function."""
    response = client.get("/api/v1/deadline/tools/get_all_jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for job in data:
        assert "id" in job
        assert "name" in job
        assert "status" in job
        assert "user" in job


def test_deadline_tools_get_workload_summary():
    """Test AI Tools API workload summary function."""
    response = client.get("/api/v1/deadline/tools/get_workload_summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_jobs" in data
    assert "running_jobs" in data
    assert "completed_jobs" in data
    assert "failed_jobs" in data
    assert "active_users" in data


def test_deadline_tools_get_jobs_by_status():
    """Test AI Tools API get jobs by status function."""
    response = client.get("/api/v1/deadline/tools/get_jobs_by_status/Completed")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deadline_tools_check_job_status():
    """Test AI Tools API check job status function."""
    # First get a job ID
    response = client.get("/api/v1/deadline/tools/get_all_jobs")
    jobs = response.json()
    
    if jobs:
        job_id = jobs[0]["id"]
        response = client.get(f"/api/v1/deadline/tools/check_job_status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        assert "is_running" in data
        assert "is_completed" in data
        assert "needs_attention" in data


def test_deadline_tools_get_failed_jobs():
    """Test AI Tools API get failed jobs function."""
    response = client.get("/api/v1/deadline/tools/get_failed_jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deadline_tools_is_system_busy():
    """Test AI Tools API system busy check function."""
    response = client.get("/api/v1/deadline/tools/is_system_busy")
    assert response.status_code == 200
    data = response.json()
    assert "is_busy" in data
    assert "total_jobs" in data
    assert "running_jobs" in data
    assert "load_percentage" in data
    assert "recommendation" in data


def test_api_separation():
    """Test that REST and Tools APIs are properly separated."""
    # REST API should have user-friendly responses
    rest_response = client.get("/api/v1/deadline/rest/status")
    rest_data = rest_response.json()
    assert "statistics" in rest_data  # User-friendly statistics
    
    # Tools API should have function-calling compatible structured data
    tools_response = client.get("/api/v1/deadline/tools/get_workload_summary")
    tools_data = tools_response.json()
    assert "total_jobs" in tools_data  # Function-calling compatible
    assert "running_jobs" in tools_data
    
    # Verify they return different data structures
    assert rest_data.keys() != tools_data.keys()


def test_function_calling_compatibility():
    """Test that AI tools endpoints are function-calling compatible."""
    # Test simple function calls with clear names
    response = client.get("/api/v1/deadline/tools/list_active_users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    
    response = client.get("/api/v1/deadline/tools/count_jobs_by_status")
    assert response.status_code == 200
    counts = response.json()
    assert isinstance(counts, dict)
    
    response = client.get("/api/v1/deadline/tools/get_running_jobs")
    assert response.status_code == 200
    running_jobs = response.json()
    assert isinstance(running_jobs, list)