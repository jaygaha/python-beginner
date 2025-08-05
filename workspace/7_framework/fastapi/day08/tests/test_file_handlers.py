import pytest
import asyncio
from fastapi import HTTPException
from pathlib import Path
import shutil
from PIL import Image
import io

# Import from the same directory or use relative imports
from src.file_handlers import FileValidator, FileStorage, ImageProcessor

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

# --- Test Fixtures ---

@pytest.fixture
def temp_uploads_dir():
    """Create a temporary directory for file storage tests and clean it up after."""
    dir_path = Path("test_uploads_temp")
    dir_path.mkdir(exist_ok=True)
    yield str(dir_path)
    if dir_path.exists():
        shutil.rmtree(dir_path)

class MockUploadFile:
    """A more realistic mock for UploadFile that handles async operations properly."""

    def __init__(self, filename: str, content: bytes, content_type: str):
        self.filename = filename
        self.content_type = content_type
        self.size = len(content)
        self._content = content
        self._position = 0

    async def read(self, size: int = -1) -> bytes:
        """Read data from the file."""
        if size == -1:
            # Read all remaining data
            data = self._content[self._position:]
            self._position = len(self._content)
        else:
            # Read up to 'size' bytes
            end_pos = min(self._position + size, len(self._content))
            data = self._content[self._position:end_pos]
            self._position = end_pos
        return data

    async def seek(self, position: int) -> None:
        """Seek to a position in the file."""
        self._position = max(0, min(position, len(self._content)))

def create_mock_upload_file(filename: str, content: bytes, content_type: str) -> MockUploadFile:
    """Helper factory to create mock UploadFile objects for testing."""
    return MockUploadFile(filename, content, content_type)

@pytest.fixture
def valid_image_file():
    """Provides a mock UploadFile representing a valid image."""
    # 1KB content, well within limits
    return create_mock_upload_file("test_image.jpg", b"a" * 1024, "image/jpeg")

@pytest.fixture
def oversized_image_file():
    """Provides a mock UploadFile representing an oversized image."""
    # Content size is 6MB, larger than the 5MB limit for images
    return create_mock_upload_file("oversized.jpg", b"a" * (6 * 1024 * 1024), "image/jpeg")

@pytest.fixture
def invalid_image_type_file():
    """Provides a mock UploadFile with a non-image content type."""
    return create_mock_upload_file("do_not_open.txt", b"some text", "text/plain")

@pytest.fixture
def valid_document_file():
    """Provides a mock UploadFile representing a valid document."""
    return create_mock_upload_file("document.pdf", b"pdf content", "application/pdf")

@pytest.fixture
def create_real_image(temp_uploads_dir):
    """Creates a real temporary image file for ImageProcessor tests."""
    image_path = Path(temp_uploads_dir) / "real_image.png"
    # Create a 150x100 red image
    img = Image.new('RGB', (150, 100), color='red')
    img.save(image_path, 'PNG')
    yield str(image_path)
    # Cleanup is handled by temp_uploads_dir fixture

@pytest.fixture(scope="session", autouse=True)
def cleanup_executor():
    """Ensure the ImageProcessor executor is cleaned up after all tests."""
    yield
    ImageProcessor.shutdown_executor()

# --- Test Suites ---

class TestFileValidator:
    """Tests for the FileValidator class."""

    async def test_validate_file_success_image(self, valid_image_file):
        """Test that a valid image file passes validation."""
        result = await FileValidator.validate_file(valid_image_file, "image")
        assert result is True

    async def test_validate_file_success_document(self, valid_document_file):
        """Test that a valid document file passes validation."""
        result = await FileValidator.validate_file(valid_document_file, "document")
        assert result is True

    async def test_validate_file_success_any_type(self, valid_image_file):
        """Test that any valid file passes when type is 'any'."""
        result = await FileValidator.validate_file(valid_image_file, "any")
        assert result is True

    async def test_validate_file_too_large(self, oversized_image_file):
        """Test that an oversized file raises an HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(oversized_image_file, "image")
        assert exc_info.value.status_code == 413
        assert "File is too large" in exc_info.value.detail

    async def test_validate_invalid_image_type(self, invalid_image_type_file):
        """Test that a file with an invalid content type for images raises an HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(invalid_image_type_file, "image")
        assert exc_info.value.status_code == 400
        assert "Invalid image type" in exc_info.value.detail

    async def test_validate_invalid_document_type(self, valid_image_file):
        """Test that a file with an invalid content type for documents raises an HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            await FileValidator.validate_file(valid_image_file, "document")
        assert exc_info.value.status_code == 400
        assert "Invalid document type" in exc_info.value.detail

    async def test_validate_file_file_pointer_reset(self, valid_image_file):
        """Test that file pointer is properly reset after validation."""
        await FileValidator.validate_file(valid_image_file, "image")
        # File should be back at the beginning
        assert valid_image_file._position == 0

        # Should be able to read the full content again
        content = await valid_image_file.read()
        assert len(content) == 1024

class TestFileStorage:
    """Tests for the FileStorage class."""

    async def test_save_file(self, temp_uploads_dir, valid_image_file):
        """Test saving a file to a category subdirectory."""
        storage = FileStorage(base_path=temp_uploads_dir)
        category = "profile_pictures"

        file_info = await storage.save_file(valid_image_file, category)

        assert file_info["original_filename"] == "test_image.jpg"
        assert file_info["file_size"] == 1024
        assert file_info["content_type"] == "image/jpeg"
        assert ".jpg" in file_info["saved_filename"]
        assert len(file_info["file_hash"]) == 64  # SHA256 hex length

        # Verify the file was physically saved in the correct location
        saved_path = Path(file_info["file_path"])
        assert saved_path.exists()
        assert saved_path.parent.name == category
        assert saved_path.read_bytes() == b"a" * 1024

    async def test_save_file_unknown_filename(self, temp_uploads_dir):
        """Test saving a file with None filename."""
        mock_file = create_mock_upload_file(None, b"test content", "text/plain")
        storage = FileStorage(base_path=temp_uploads_dir)

        file_info = await storage.save_file(mock_file, "temp")
        assert file_info["original_filename"] == "unknown"

    async def test_save_file_creates_directory(self, temp_uploads_dir):
        """Test that save_file creates the category directory if it doesn't exist."""
        storage = FileStorage(base_path=temp_uploads_dir)
        category = "new_category"
        mock_file = create_mock_upload_file("test.txt", b"content", "text/plain")

        file_info = await storage.save_file(mock_file, category)

        category_path = Path(temp_uploads_dir) / category
        assert category_path.exists()
        assert category_path.is_dir()

    async def test_delete_file(self, temp_uploads_dir, valid_image_file):
        """Test that a file can be successfully deleted."""
        storage = FileStorage(base_path=temp_uploads_dir)
        file_info = await storage.save_file(valid_image_file, "temp")
        file_path = file_info["file_path"]

        assert Path(file_path).exists()
        delete_success = await storage.delete_file(file_path)
        assert delete_success is True
        assert not Path(file_path).exists()

    async def test_delete_nonexistent_file(self, temp_uploads_dir):
        """Test that attempting to delete a non-existent file returns False."""
        storage = FileStorage(base_path=temp_uploads_dir)
        result = await storage.delete_file("non/existent/path.txt")
        assert result is False

    async def test_delete_directory_instead_of_file(self, temp_uploads_dir):
        """Test that attempting to delete a directory returns False."""
        storage = FileStorage(base_path=temp_uploads_dir)
        directory_path = Path(temp_uploads_dir) / "test_dir"
        directory_path.mkdir()

        result = await storage.delete_file(str(directory_path))
        assert result is False

    async def test_get_file_path(self, temp_uploads_dir):
        """Test the get_file_path method."""
        storage = FileStorage(base_path=temp_uploads_dir)
        path = storage.get_file_path("test.jpg", "images")

        expected_path = Path(temp_uploads_dir) / "images" / "test.jpg"
        assert path == expected_path

class TestImageProcessor:
    """Tests for the ImageProcessor class."""

    async def test_get_image_info(self, create_real_image):
        """Test that image metadata (width, height) is read correctly."""
        info = await ImageProcessor.get_image_info(create_real_image)
        assert info["width"] == 150
        assert info["height"] == 100

    async def test_create_thumbnail(self, create_real_image, temp_uploads_dir):
        """Test that a thumbnail is created with the correct dimensions."""
        thumbnail_dir = Path(temp_uploads_dir) / "thumbnails"
        thumbnail_path = thumbnail_dir / "thumb_real_image.png"

        await ImageProcessor.create_thumbnail(create_real_image, str(thumbnail_path))

        assert thumbnail_path.exists()
        with Image.open(thumbnail_path) as thumb:
            # The thumbnail should be resized to fit within the max dimensions while maintaining aspect ratio
            assert thumb.size[0] <= ImageProcessor.THUMBNAIL_SIZE[0]
            assert thumb.size[1] <= ImageProcessor.THUMBNAIL_SIZE[1]
            # Original is 150x100, aspect ratio 1.5
            # Thumbnail max is 128x128, so it should be 128x85 (128/1.5 ≈ 85.33, rounded down to 85)
            assert thumb.size == (128, 85)

    async def test_create_thumbnail_creates_directory(self, create_real_image, temp_uploads_dir):
        """Test that create_thumbnail creates the destination directory if it doesn't exist."""
        thumbnail_path = Path(temp_uploads_dir) / "deep" / "nested" / "path" / "thumb.png"

        await ImageProcessor.create_thumbnail(create_real_image, str(thumbnail_path))

        assert thumbnail_path.exists()
        assert thumbnail_path.parent.exists()

    async def test_get_image_info_on_invalid_file(self, temp_uploads_dir):
        """Test that getting info from a non-image file raises an HTTPException."""
        not_an_image_path = Path(temp_uploads_dir) / "fake.txt"
        not_an_image_path.write_text("I am not an image")

        with pytest.raises(HTTPException) as exc_info:
            await ImageProcessor.get_image_info(str(not_an_image_path))
        assert exc_info.value.status_code == 500

    async def test_create_thumbnail_on_invalid_file(self, temp_uploads_dir):
        """Test that creating thumbnail from a non-image file raises an HTTPException."""
        not_an_image_path = Path(temp_uploads_dir) / "fake.txt"
        not_an_image_path.write_text("I am not an image")
        thumbnail_path = Path(temp_uploads_dir) / "thumb.png"

        with pytest.raises(HTTPException) as exc_info:
            await ImageProcessor.create_thumbnail(str(not_an_image_path), str(thumbnail_path))
        assert exc_info.value.status_code == 500

    async def test_get_image_info_nonexistent_file(self):
        """Test that getting info from a non-existent file raises an HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            await ImageProcessor.get_image_info("nonexistent/file.jpg")
        assert exc_info.value.status_code == 500

# --- Integration Tests ---

class TestIntegration:
    """Integration tests for the complete file handling workflow."""

    async def test_complete_image_workflow(self, temp_uploads_dir):
        """Test the complete workflow: validate -> save -> process -> delete."""
        # Create a real small image in memory
        img = Image.new('RGB', (100, 80), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Create mock upload file with real image data
        upload_file = create_mock_upload_file("test.png", img_bytes.getvalue(), "image/png")

        # Step 1: Validate
        validator_result = await FileValidator.validate_file(upload_file, "image")
        assert validator_result is True

        # Step 2: Save
        storage = FileStorage(base_path=temp_uploads_dir)
        file_info = await storage.save_file(upload_file, "images")

        assert Path(file_info["file_path"]).exists()

        # Step 3: Process
        image_info = await ImageProcessor.get_image_info(file_info["file_path"])
        assert image_info["width"] == 100
        assert image_info["height"] == 80

        thumbnail_path = Path(temp_uploads_dir) / "thumbnails" / "thumb.png"
        await ImageProcessor.create_thumbnail(file_info["file_path"], str(thumbnail_path))
        assert thumbnail_path.exists()

        # Step 4: Cleanup
        delete_result = await storage.delete_file(file_info["file_path"])
        assert delete_result is True
        assert not Path(file_info["file_path"]).exists()

    async def test_concurrent_file_operations(self, temp_uploads_dir):
        """Test that multiple file operations can run concurrently without issues."""
        storage = FileStorage(base_path=temp_uploads_dir)

        # Create multiple mock files
        files = [
            create_mock_upload_file(f"file_{i}.txt", f"content_{i}".encode(), "text/plain")
            for i in range(5)
        ]

        # Save all files concurrently
        tasks = [storage.save_file(file, "concurrent") for file in files]
        results = await asyncio.gather(*tasks)

        # Verify all files were saved
        assert len(results) == 5
        for result in results:
            assert Path(result["file_path"]).exists()

        # Delete all files concurrently
        delete_tasks = [storage.delete_file(result["file_path"]) for result in results]
        delete_results = await asyncio.gather(*delete_tasks)

        # Verify all files were deleted
        assert all(delete_results)
        for result in results:
            assert not Path(result["file_path"]).exists()
