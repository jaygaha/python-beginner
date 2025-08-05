import pytest
from datetime import datetime, timezone
from typing import Dict, Any
from pydantic import ValidationError
import json

# Import the models (assuming they're in a models.py file in the same directory)
from src.models import FileUploadResponse, ImageUploadResponse, FileMetadata, BatchUploadResponse


class TestFileUploadResponse:
    """Test cases for FileUploadResponse model."""

    def test_file_upload_response_creation_valid(self):
        """Test creating a valid FileUploadResponse."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "12345",
            "original_filename": "test.pdf",
            "saved_filename": "uuid-12345.pdf",
            "file_size": 1024,
            "content_type": "application/pdf",
            "file_hash": "abc123def456",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/files/uuid-12345.pdf"
        }

        response = FileUploadResponse(**data)

        assert response.id == "12345"
        assert response.original_filename == "test.pdf"
        assert response.saved_filename == "uuid-12345.pdf"
        assert response.file_size == 1024
        assert response.content_type == "application/pdf"
        assert response.file_hash == "abc123def456"
        assert response.upload_timestamp == timestamp
        assert response.file_url == "https://example.com/files/uuid-12345.pdf"

    def test_file_upload_response_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        incomplete_data = {
            "id": "12345",
            "original_filename": "test.pdf",
            # Missing other required fields
        }

        with pytest.raises(ValidationError) as exc_info:
            FileUploadResponse(**incomplete_data)

        errors = exc_info.value.errors()
        required_fields = {"saved_filename", "file_size", "content_type", "file_hash", "upload_timestamp", "file_url"}
        error_fields = {error["loc"][0] for error in errors if error["type"] == "missing"}

        assert required_fields.issubset(error_fields)

    def test_file_upload_response_invalid_types(self):
        """Test that invalid field types raise ValidationError."""
        invalid_data = {
            "id": "12345",
            "original_filename": "test.pdf",
            "saved_filename": "uuid-12345.pdf",
            "file_size": "not_an_int",  # Should be int
            "content_type": "application/pdf",
            "file_hash": "abc123def456",
            "upload_timestamp": "not_a_datetime",  # Should be datetime
            "file_url": "https://example.com/files/uuid-12345.pdf"
        }

        with pytest.raises(ValidationError) as exc_info:
            FileUploadResponse(**invalid_data)

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}

        assert "file_size" in error_fields
        assert "upload_timestamp" in error_fields

    def test_file_upload_response_serialization(self):
        """Test that the model can be serialized to JSON."""
        timestamp = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        data = {
            "id": "12345",
            "original_filename": "test.pdf",
            "saved_filename": "uuid-12345.pdf",
            "file_size": 1024,
            "content_type": "application/pdf",
            "file_hash": "abc123def456",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/files/uuid-12345.pdf"
        }

        response = FileUploadResponse(**data)
        json_str = response.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["id"] == "12345"
        assert parsed["file_size"] == 1024
        assert "upload_timestamp" in parsed

    def test_file_upload_response_negative_file_size(self):
        """Test that negative file sizes are handled."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "12345",
            "original_filename": "test.pdf",
            "saved_filename": "uuid-12345.pdf",
            "file_size": -100,  # Negative size
            "content_type": "application/pdf",
            "file_hash": "abc123def456",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/files/uuid-12345.pdf"
        }

        # Pydantic allows negative integers by default
        response = FileUploadResponse(**data)
        assert response.file_size == -100


class TestImageUploadResponse:
    """Test cases for ImageUploadResponse model."""

    def test_image_upload_response_creation_complete(self):
        """Test creating an ImageUploadResponse with all fields."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "img123",
            "original_filename": "photo.jpg",
            "saved_filename": "uuid-img123.jpg",
            "file_size": 2048,
            "content_type": "image/jpeg",
            "file_hash": "def456ghi789",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/images/uuid-img123.jpg",
            "width": 1920,
            "height": 1080,
            "thumbnail_url": "https://example.com/thumbnails/uuid-img123.jpg"
        }

        response = ImageUploadResponse(**data)

        # Test inherited fields
        assert response.id == "img123"
        assert response.original_filename == "photo.jpg"
        assert response.file_size == 2048

        # Test image-specific fields
        assert response.width == 1920
        assert response.height == 1080
        assert response.thumbnail_url == "https://example.com/thumbnails/uuid-img123.jpg"

    def test_image_upload_response_optional_fields_none(self):
        """Test that optional image fields can be None."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "img123",
            "original_filename": "photo.jpg",
            "saved_filename": "uuid-img123.jpg",
            "file_size": 2048,
            "content_type": "image/jpeg",
            "file_hash": "def456ghi789",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/images/uuid-img123.jpg",
            # width, height, thumbnail_url are optional
        }

        response = ImageUploadResponse(**data)

        assert response.width is None
        assert response.height is None
        assert response.thumbnail_url is None

    def test_image_upload_response_inheritance(self):
        """Test that ImageUploadResponse properly inherits from FileUploadResponse."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "img123",
            "original_filename": "photo.jpg",
            "saved_filename": "uuid-img123.jpg",
            "file_size": 2048,
            "content_type": "image/jpeg",
            "file_hash": "def456ghi789",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/images/uuid-img123.jpg",
            "width": 800,
            "height": 600
        }

        response = ImageUploadResponse(**data)

        # Should be instance of both classes
        assert isinstance(response, ImageUploadResponse)
        assert isinstance(response, FileUploadResponse)

    def test_image_upload_response_invalid_dimensions(self):
        """Test handling of invalid image dimensions."""
        timestamp = datetime.now(timezone.utc)
        data = {
            "id": "img123",
            "original_filename": "photo.jpg",
            "saved_filename": "uuid-img123.jpg",
            "file_size": 2048,
            "content_type": "image/jpeg",
            "file_hash": "def456ghi789",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/images/uuid-img123.jpg",
            "width": "not_an_int",
            "height": "also_not_an_int"
        }

        with pytest.raises(ValidationError) as exc_info:
            ImageUploadResponse(**data)

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}
        assert "width" in error_fields
        assert "height" in error_fields


class TestFileMetadata:
    """Test cases for FileMetadata model."""

    def test_file_metadata_creation_complete(self):
        """Test creating FileMetadata with all fields."""
        upload_date = datetime.now(timezone.utc)
        data = {
            "filename": "document.pdf",
            "size": 5120,
            "content_type": "application/pdf",
            "upload_date": upload_date,
            "uploader": "user123"
        }

        metadata = FileMetadata(**data)

        assert metadata.filename == "document.pdf"
        assert metadata.size == 5120
        assert metadata.content_type == "application/pdf"
        assert metadata.upload_date == upload_date
        assert metadata.uploader == "user123"

    def test_file_metadata_optional_uploader(self):
        """Test that uploader field is optional."""
        upload_date = datetime.now(timezone.utc)
        data = {
            "filename": "document.pdf",
            "size": 5120,
            "content_type": "application/pdf",
            "upload_date": upload_date,
            # uploader is optional
        }

        metadata = FileMetadata(**data)
        assert metadata.uploader is None

    def test_file_metadata_empty_strings(self):
        """Test handling of empty strings."""
        upload_date = datetime.now(timezone.utc)
        data = {
            "filename": "",  # Empty filename
            "size": 0,
            "content_type": "",  # Empty content type
            "upload_date": upload_date,
            "uploader": ""  # Empty uploader
        }

        metadata = FileMetadata(**data)
        assert metadata.filename == ""
        assert metadata.content_type == ""
        assert metadata.uploader == ""

    def test_file_metadata_zero_size(self):
        """Test that zero file size is valid."""
        upload_date = datetime.now(timezone.utc)
        data = {
            "filename": "empty.txt",
            "size": 0,
            "content_type": "text/plain",
            "upload_date": upload_date
        }

        metadata = FileMetadata(**data)
        assert metadata.size == 0


class TestBatchUploadResponse:
    """Test cases for BatchUploadResponse model."""

    def test_batch_upload_response_creation_complete(self):
        """Test creating a complete BatchUploadResponse."""
        timestamp = datetime.now(timezone.utc)
        successful_upload = FileUploadResponse(
            id="success1",
            original_filename="file1.pdf",
            saved_filename="uuid-success1.pdf",
            file_size=1024,
            content_type="application/pdf",
            file_hash="hash123",
            upload_timestamp=timestamp,
            file_url="https://example.com/success1.pdf"
        )

        failed_upload = {
            "filename": "file2.pdf",
            "error": "File too large",
            "error_code": "FILE_TOO_LARGE"
        }

        data = {
            "successful_uploads": [successful_upload],
            "failed_uploads": [failed_upload],
            "total_files": 2,
            "success_count": 1,
            "failure_count": 1
        }

        batch = BatchUploadResponse(**data)

        assert len(batch.successful_uploads) == 1
        assert len(batch.failed_uploads) == 1
        assert batch.total_files == 2
        assert batch.success_count == 1
        assert batch.failure_count == 1
        assert batch.successful_uploads[0].id == "success1"
        assert batch.failed_uploads[0]["error"] == "File too large"

    def test_batch_upload_response_empty_lists(self):
        """Test BatchUploadResponse with empty lists."""
        data = {
            "successful_uploads": [],
            "failed_uploads": [],
            "total_files": 0,
            "success_count": 0,
            "failure_count": 0
        }

        batch = BatchUploadResponse(**data)

        assert batch.successful_uploads == []
        assert batch.failed_uploads == []
        assert batch.total_files == 0
        assert batch.success_count == 0
        assert batch.failure_count == 0

    def test_batch_upload_response_only_successes(self):
        """Test BatchUploadResponse with only successful uploads."""
        timestamp = datetime.now(timezone.utc)
        successful_uploads = [
            FileUploadResponse(
                id=f"success{i}",
                original_filename=f"file{i}.pdf",
                saved_filename=f"uuid-success{i}.pdf",
                file_size=1024 * i,
                content_type="application/pdf",
                file_hash=f"hash{i}",
                upload_timestamp=timestamp,
                file_url=f"https://example.com/success{i}.pdf"
            )
            for i in range(1, 4)
        ]

        data = {
            "successful_uploads": successful_uploads,
            "failed_uploads": [],
            "total_files": 3,
            "success_count": 3,
            "failure_count": 0
        }

        batch = BatchUploadResponse(**data)

        assert len(batch.successful_uploads) == 3
        assert len(batch.failed_uploads) == 0
        assert batch.total_files == 3
        assert batch.success_count == 3
        assert batch.failure_count == 0

    def test_batch_upload_response_only_failures(self):
        """Test BatchUploadResponse with only failed uploads."""
        failed_uploads = [
            {"filename": "file1.pdf", "error": "File too large"},
            {"filename": "file2.jpg", "error": "Invalid format"},
            {"filename": "file3.doc", "error": "Corrupted file"}
        ]

        data = {
            "successful_uploads": [],
            "failed_uploads": failed_uploads,
            "total_files": 3,
            "success_count": 0,
            "failure_count": 3
        }

        batch = BatchUploadResponse(**data)

        assert len(batch.successful_uploads) == 0
        assert len(batch.failed_uploads) == 3
        assert batch.total_files == 3
        assert batch.success_count == 0
        assert batch.failure_count == 3

    def test_batch_upload_response_count_mismatch(self):
        """Test that count mismatches are still accepted (validation could be added)."""
        timestamp = datetime.now(timezone.utc)
        successful_upload = FileUploadResponse(
            id="success1",
            original_filename="file1.pdf",
            saved_filename="uuid-success1.pdf",
            file_size=1024,
            content_type="application/pdf",
            file_hash="hash123",
            upload_timestamp=timestamp,
            file_url="https://example.com/success1.pdf"
        )

        data = {
            "successful_uploads": [successful_upload],
            "failed_uploads": [],
            "total_files": 5,  # Mismatch: should be 1
            "success_count": 3,  # Mismatch: should be 1
            "failure_count": 2   # Mismatch: should be 0
        }

        # This will pass with basic Pydantic validation
        # In a real application, you might want custom validators
        batch = BatchUploadResponse(**data)

        assert batch.total_files == 5
        assert batch.success_count == 3
        assert batch.failure_count == 2

    def test_batch_upload_response_invalid_successful_upload(self):
        """Test that invalid successful uploads raise ValidationError."""
        invalid_upload = {
            "id": "invalid",
            # Missing required fields for FileUploadResponse
        }

        data = {
            "successful_uploads": [invalid_upload],
            "failed_uploads": [],
            "total_files": 1,
            "success_count": 1,
            "failure_count": 0
        }

        with pytest.raises(ValidationError):
            BatchUploadResponse(**data)


class TestModelIntegration:
    """Integration tests for model interactions."""

    def test_models_serialization_roundtrip(self):
        """Test that models can be serialized and deserialized."""
        timestamp = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Create an ImageUploadResponse
        image_response = ImageUploadResponse(
            id="img123",
            original_filename="photo.jpg",
            saved_filename="uuid-img123.jpg",
            file_size=2048,
            content_type="image/jpeg",
            file_hash="hash123",
            upload_timestamp=timestamp,
            file_url="https://example.com/img123.jpg",
            width=1920,
            height=1080,
            thumbnail_url="https://example.com/thumb123.jpg"
        )

        # Serialize and deserialize
        json_data = image_response.model_dump()
        recreated = ImageUploadResponse(**json_data)

        assert recreated.id == image_response.id
        assert recreated.width == image_response.width
        assert recreated.height == image_response.height
        assert recreated.upload_timestamp == image_response.upload_timestamp

    def test_batch_with_mixed_response_types(self):
        """Test BatchUploadResponse with different types of successful uploads."""
        timestamp = datetime.now(timezone.utc)

        # Note: In practice, you might want all successful_uploads to be the same type
        # or use a Union type. This test assumes they're all FileUploadResponse or subclasses
        file_response = FileUploadResponse(
            id="file1",
            original_filename="doc.pdf",
            saved_filename="uuid-file1.pdf",
            file_size=1024,
            content_type="application/pdf",
            file_hash="hash1",
            upload_timestamp=timestamp,
            file_url="https://example.com/file1.pdf"
        )

        image_response = ImageUploadResponse(
            id="img1",
            original_filename="photo.jpg",
            saved_filename="uuid-img1.jpg",
            file_size=2048,
            content_type="image/jpeg",
            file_hash="hash2",
            upload_timestamp=timestamp,
            file_url="https://example.com/img1.jpg",
            width=800,
            height=600
        )

        # Convert to dict to simulate mixed types in a list
        batch_data = {
            "successful_uploads": [
                file_response.model_dump(),
                image_response.model_dump()
            ],
            "failed_uploads": [],
            "total_files": 2,
            "success_count": 2,
            "failure_count": 0
        }

        # This will create FileUploadResponse objects from the dicts
        batch = BatchUploadResponse(**batch_data)

        assert len(batch.successful_uploads) == 2
        assert batch.successful_uploads[0].id == "file1"
        assert batch.successful_uploads[1].id == "img1"

    def test_model_field_validation_edge_cases(self):
        """Test edge cases for model field validation."""
        timestamp = datetime.now(timezone.utc)

        # Test with very long strings
        long_filename = "a" * 1000
        data = {
            "id": "test123",
            "original_filename": long_filename,
            "saved_filename": "uuid-test123.txt",
            "file_size": 0,
            "content_type": "text/plain",
            "file_hash": "hash123",
            "upload_timestamp": timestamp,
            "file_url": "https://example.com/test123.txt"
        }

        response = FileUploadResponse(**data)
        assert response.original_filename == long_filename
        assert len(response.original_filename) == 1000
