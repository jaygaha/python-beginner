import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil
import os
from PIL import Image

# This assumes the tests are run from the root of the 'day08' directory or a configured test runner.
# Adjust the path if your test runner has a different working directory.
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import app, file_storage, files_db

# --- Test Setup and Fixtures ---

@pytest.fixture(scope="module")
def client():
    """
    Yield a TestClient instance that can be used to make requests to the application.
    This client is reused for all tests in this module for efficiency.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def setup_and_teardown_test_environment():
    """
    This fixture runs for every test function. It sets up a temporary upload
    directory, monkeypatches the file storage to use it, and clears the in-memory
    database. After the test, it cleans up the temporary directory.
    """
    # Define a temporary directory for test uploads
    test_upload_dir = Path("test_uploads_temp")
    test_upload_dir.mkdir(exist_ok=True, parents=True)

    # Monkeypatch the file_storage object to use this temporary directory
    original_base_path = file_storage.base_path
    file_storage.base_path = test_upload_dir

    # Clear the in-memory database to ensure test isolation
    files_db.clear()

    # Yield control to the test function
    yield

    # Teardown: Clean up the created resources
    shutil.rmtree(test_upload_dir, ignore_errors=True)
    # Restore the original path (good practice)
    file_storage.base_path = original_base_path


# --- Helper Function ---

def create_dummy_image(path: Path, size=(100, 80), color='blue'):
    """Creates a small dummy image file for testing."""
    img = Image.new('RGB', size, color=color)
    img.save(path)
    return path

# --- Test Cases ---

def test_health_check(client: TestClient):
    """Test the /health endpoint for a successful response."""
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert json_response["total_files"] == 0
    assert json_response["upload_directory_exists"] is True

def test_upload_single_file(client: TestClient):
    """Test uploading a single file to the /upload/single/ endpoint."""
    file_content = b"This is a test file."
    response = client.post(
        "/upload/single/",
        files={"file": ("test_single.txt", file_content, "text/plain")},
        data={"description": "A test for single upload"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original_filename"] == "test_single.txt"
    assert json_response["content_type"] == "text/plain"
    assert "file_url" in json_response
    # Verify the file exists on disk in the 'general' category
    saved_filename = json_response["saved_filename"]
    assert (file_storage.base_path / "general" / saved_filename).exists()

def test_upload_image_with_thumbnail(client: TestClient):
    """Test uploading an image and creating a thumbnail via /upload/image/."""
    dummy_image_path = create_dummy_image(file_storage.base_path / "temp_image.png")

    with open(dummy_image_path, "rb") as f:
        response = client.post(
            "/upload/image/",
            files={"image": ("my_avatar.png", f, "image/png")},
            data={"create_thumbnail": "true", "alt_text": "A test image"}
        )

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["original_filename"] == "my_avatar.png"
    assert json_response["width"] == 100
    assert json_response["height"] == 80
    assert json_response["thumbnail_url"] is not None

    # Verify the image and its thumbnail were created on disk
    saved_filename = json_response["saved_filename"]
    thumbnail_filename = Path(json_response["thumbnail_url"]).name
    assert (file_storage.base_path / "images" / saved_filename).exists()
    assert (file_storage.base_path / "thumbnails" / thumbnail_filename).exists()

def test_upload_multiple_files(client: TestClient):
    """Test uploading multiple files to /upload/multiple/."""
    files_to_upload = [
        ("files", ("file1.txt", b"content1", "text/plain")),
        ("files", ("file2.txt", b"content2", "text/plain")),
    ]
    response = client.post("/upload/multiple/", files=files_to_upload, data={"category": "batch"})

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total_files"] == 2
    assert json_response["success_count"] == 2
    assert json_response["failure_count"] == 0
    assert len(json_response["successful_uploads"]) == 2

    # Verify files were saved in the correct category directory
    for upload in json_response["successful_uploads"]:
        saved_filename = upload["saved_filename"]
        assert (file_storage.base_path / "batch" / saved_filename).exists()

def test_file_info_download_stream_and_delete(client: TestClient):
    """Test the full lifecycle of a file: info, download, stream, and delete."""
    # 1. Upload a file to work with
    upload_response = client.post(
        "/upload/single/",
        files={"file": ("lifecycle.txt", b"lifecycle content", "text/plain")}
    )
    file_id = upload_response.json()["id"]
    saved_filename = upload_response.json()["saved_filename"]
    saved_path = file_storage.base_path / "general" / saved_filename
    assert saved_path.exists()

    # 2. Get file info
    info_response = client.get(f"/files/{file_id}")
    assert info_response.status_code == 200
    assert info_response.json()["id"] == file_id
    assert info_response.json()["original_filename"] == "lifecycle.txt"

    # 3. Download the file
    download_response = client.get(f"/files/{file_id}/download")
    assert download_response.status_code == 200
    assert download_response.content == b"lifecycle content"
    assert download_response.headers["content-disposition"] == 'attachment; filename="lifecycle.txt"'

    # 4. Stream the file
    stream_response = client.get(f"/files/{file_id}/stream")
    assert stream_response.status_code == 200
    assert stream_response.content == b"lifecycle content"
    assert "inline" in stream_response.headers["content-disposition"]

    # 5. Delete the file
    delete_response = client.delete(f"/files/{file_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "File deleted successfully"

    # 6. Verify it's gone from DB and disk
    assert file_id not in files_db
    assert not saved_path.exists()

    # 7. Verify subsequent requests for the file fail
    assert client.get(f"/files/{file_id}").status_code == 404
    assert client.get(f"/files/{file_id}/download").status_code == 404

def test_search_files(client: TestClient):
    """Test file search functionality with and without filters."""
    # Upload some files to search through
    client.post("/upload/single/", files={"file": ("project_report_final.pdf", b"pdf content", "application/pdf")})
    client.post("/upload/document/", files={"document": ("project_summary.txt", b"txt content", "text/plain")}, data={"title": "Project Summary"})
    client.post("/upload/single/", files={"file": ("annual_report.docx", b"doc content", "application/msword")})

    # Search for "report" - should match 2 files
    search_response = client.post("/files/search", json={"query": "report"})
    assert search_response.status_code == 200
    results = search_response.json()["results"]
    assert len(results) == 2

    # Search for "project" with a content type filter - should match 1 file
    search_response_filtered = client.post("/files/search", json={
        "query": "project",
        "content_types": ["application/pdf"]
    })
    assert search_response_filtered.status_code == 200
    results_filtered = search_response_filtered.json()["results"]
    assert len(results_filtered) == 1
    assert results_filtered[0]["original_filename"] == "project_report_final.pdf"

    # Search with size filter (all files are tiny, so min_size should find them)
    search_response_min_size = client.post("/files/search", json={"query": "report", "min_size": 1})
    assert len(search_response_min_size.json()["results"]) == 2

    # Search with size filter that excludes all files
    search_response_max_size = client.post("/files/search", json={"query": "report", "max_size": 1})
    assert len(search_response_max_size.json()["results"]) == 0

def test_get_file_metadata(client: TestClient):
    """Test retrieving file metadata from the /files/{file_id}/metadata endpoint."""
    upload_response = client.post(
        "/upload/single/",
        files={"file": ("metadata_test.txt", b"some data", "text/plain")}
    )
    file_id = upload_response.json()["id"]

    response = client.get(f"/files/{file_id}/metadata")
    assert response.status_code == 200
    metadata = response.json()
    assert metadata["file_exists"] is True
    assert metadata["file_size_on_disk"] == len(b"some data")
    assert metadata["recorded_size"] == len(b"some data")
    assert "last_modified" in metadata
    assert metadata["file_hash"] is not None

def test_file_not_found_errors(client: TestClient):
    """Test that requesting a non-existent file ID returns a 404 Not Found."""
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    endpoints = [
        f"/files/{non_existent_id}",
        f"/files/{non_existent_id}/download",
        f"/files/{non_existent_id}/stream",
        f"/files/{non_existent_id}/metadata",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 404
        assert response.json()["detail"] == "File not found"

    # Test delete on non-existent file
    response = client.delete(f"/files/{non_existent_id}")
    assert response.status_code == 404
