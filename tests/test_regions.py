"""
Tests for regional functionality.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_current_region_default():
    """Test getting current region info with default region."""
    response = client.get("/api/v1/regions/current")
    assert response.status_code == 200
    data = response.json()
    assert "region_code" in data
    assert "region_name" in data
    assert "timezone" in data


def test_get_current_region_with_header():
    """Test getting current region info with X-Region header."""
    response = client.get(
        "/api/v1/regions/current",
        headers={"X-Region": "eu-west"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["region_code"] == "eu-west"
    assert data["region_name"] == "EU West"
    assert data["timezone"] == "Europe/London"


def test_list_available_regions():
    """Test listing all available regions."""
    response = client.get("/api/v1/regions/available")
    assert response.status_code == 200
    data = response.json()
    assert "us-east" in data
    assert "eu-west" in data
    assert "asia-pacific" in data


def test_get_region_config():
    """Test getting specific region configuration."""
    response = client.get("/api/v1/regions/us-east/config")
    assert response.status_code == 200
    data = response.json()
    assert data["region_code"] == "us-east"
    assert data["currency"] == "USD"
    assert "features_enabled" in data


def test_deadline_jobs_default_region():
    """Test getting deadline jobs from default region."""
    response = client.get("/api/v1/deadline/jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deadline_jobs_specific_region():
    """Test getting deadline jobs with specific region header."""
    response = client.get(
        "/api/v1/deadline/jobs",
        headers={"X-Region": "eu-west"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check that response headers include region info
    assert response.headers.get("X-Region") == "eu-west"


def test_deadline_status():
    """Test getting deadline service status."""
    response = client.get("/api/v1/deadline/status")
    assert response.status_code == 200
    data = response.json()
    assert "region" in data
    assert "service_available" in data
    assert "features" in data


def test_region_feature_requirement():
    """Test that advanced analytics feature is required for cross-region access."""
    # This should work for US East (has advanced_analytics enabled)
    response = client.get(
        "/api/v1/deadline/jobs/region/eu-west",
        headers={"X-Region": "us-east"}
    )
    assert response.status_code == 200
    
    # This should fail for EU West (advanced_analytics disabled)
    response = client.get(
        "/api/v1/deadline/jobs/region/us-east",
        headers={"X-Region": "eu-west"}
    )
    assert response.status_code == 403