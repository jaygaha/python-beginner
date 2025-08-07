import time
import os
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    """
    Pytest fixture to create a TestClient.
    Using a `with` statement ensures that the application's lifespan
    (startup and shutdown events) is handled correctly.
    """
    with TestClient(app) as c:
        yield c

def test_read_root(client):
    """
    Test the root endpoint to ensure the API is running.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}

def test_caching(client):
    """
    Test the caching functionality.
    - The first request should take ~2 seconds.
    - The second request should be much faster due to the cache.
    - The data from both requests should be identical.
    """
    # First request - should be slow and not from cache
    start_time = time.time()
    response1 = client.get("/cached-data")
    duration1 = time.time() - start_time

    assert response1.status_code == 200
    assert duration1 >= 2.0
    data1 = response1.json()

    # Second request - should be fast and from cache
    start_time = time.time()
    response2 = client.get("/cached-data")
    duration2 = time.time() - start_time

    assert response2.status_code == 200
    assert duration2 < 1.0  # Should be significantly faster
    data2 = response2.json()

    # The timestamp should be the same, proving it's cached data
    assert data1["timestamp"] == data2["timestamp"]

def test_rate_limiting(client):
    """
    Test the rate limiting functionality.
    - The first 5 requests should succeed (200 OK).
    - The 6th request should fail with a 429 Too Many Requests error.
    """
    # Make 5 successful requests
    for i in range(5):
        response = client.get("/rate-limited")
        assert response.status_code == 200, f"Request {i+1} failed unexpectedly"

    # The 6th request should be rate-limited
    response = client.get("/rate-limited")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]

def test_background_task(client):
    """
    Test the background task endpoint.
    - The endpoint should return an immediate success response.
    - The background task should create/write to a log file.
    """
    log_file = "log.txt"
    # Clean up log file before test if it exists
    if os.path.exists(log_file):
        os.remove(log_file)

    # Trigger the background task
    response = client.post("/background-task")
    assert response.status_code == 200
    assert response.json() == {"message": "Background task has been initiated."}

    # Give the background task a moment to run
    time.sleep(0.5)

    # Check if the log file was created and contains the correct message
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
        assert "Processing data in the background" in content

    # Clean up the log file after the test
    os.remove(log_file)
