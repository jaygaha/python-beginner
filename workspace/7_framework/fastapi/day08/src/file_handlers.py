from fastapi import UploadFile, HTTPException, status
from PIL import Image
import aiofiles
import os
import uuid
from typing import Dict, Optional
import hashlib
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

class FileValidator:
    """
    Validates files based on size and content type.
    """
    ALLOWED_IMAGE_TYPES = {
        "image/jpeg", "image/png", "image/gif", "image/webp"
    }
    ALLOWED_DOCUMENT_TYPES = {
        "application/pdf", "text/plain", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB

    @classmethod
    async def validate_file(cls, file: UploadFile, file_type: str = "any") -> bool:
        """
        Validates the uploaded file against size and type constraints.

        Args:
            file: The uploaded file object from FastAPI.
            file_type: A string indicating the type of file to validate against
                       ('any', 'image', 'document').

        Returns:
            True if the file is valid.

        Raises:
            HTTPException: If the file is too large or has an invalid content type.
        """
        # Validate content type first (no need to read file for this)
        if file_type == "image" and file.content_type not in cls.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image type. Allowed types are: {', '.join(cls.ALLOWED_IMAGE_TYPES)}"
            )

        if file_type == "document" and file.content_type not in cls.ALLOWED_DOCUMENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document type. Allowed types are: {', '.join(cls.ALLOWED_DOCUMENT_TYPES)}"
            )

        # Check file size by reading in chunks (more memory efficient)
        max_size = cls.MAX_IMAGE_SIZE if file_type == "image" else cls.MAX_FILE_SIZE
        size = 0

        try:
            await file.seek(0)  # Ensure we start from the beginning
            while True:
                chunk = await file.read(8192)  # Read in 8KB chunks
                if not chunk:
                    break
                size += len(chunk)

                # Early exit if file is too large
                if size > max_size:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File is too large. Max size for {file_type} is {max_size // 1024 // 1024}MB."
                    )

            # Reset file pointer for subsequent operations
            await file.seek(0)
            return True

        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error reading file: {str(e)}"
            )

class FileStorage:
    """
    Handles the storage of files on the filesystem.
    """
    def __init__(self, base_path: str = "uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True, parents=True)

    def get_file_path(self, filename: str, category: str) -> Path:
        """
        Constructs the full path for a file within a specific category.
        """
        category_path = self.base_path / category
        return category_path / filename

    async def save_file(self, file: UploadFile, category: str) -> Dict:
        """
        Saves an uploaded file to disk, calculates its hash, and returns its metadata.

        Args:
            file: The uploaded file to save.
            category: The sub-directory where the file will be stored.

        Returns:
            A dictionary containing the file's metadata.
        """
        file_path: Optional[Path] = None

        try:
            category_path = self.base_path / category
            category_path.mkdir(exist_ok=True, parents=True)

            # Ensure file.filename is not None
            original_filename = file.filename if file.filename is not None else "unknown"
            file_extension = Path(original_filename).suffix
            saved_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = category_path / saved_filename

            # Ensure file pointer is at the beginning
            await file.seek(0)

            sha256_hash = hashlib.sha256()
            file_size = 0

            async with aiofiles.open(file_path, 'wb') as f:
                while True:
                    chunk = await file.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    await f.write(chunk)
                    sha256_hash.update(chunk)
                    file_size += len(chunk)

            return {
                "original_filename": original_filename,
                "saved_filename": saved_filename,
                "file_path": str(file_path),
                "file_size": file_size,
                "content_type": file.content_type,
                "file_hash": sha256_hash.hexdigest(),
            }

        except Exception as e:
            # Clean up partial file if it was created
            if file_path is not None and file_path.exists():
                try:
                    os.remove(file_path)
                except OSError:
                    pass  # Log this in production

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )

    async def delete_file(self, file_path: str) -> bool:
        """
        Deletes a file from the disk.

        Args:
            file_path: The full path of the file to delete.

        Returns:
            True if the file was deleted successfully, False otherwise.
        """
        path = Path(file_path)
        if path.exists() and path.is_file():
            try:
                os.remove(path)
                return True
            except OSError as e:
                # In a real application, this error should be logged.
                # logger.error(f"Failed to delete file {file_path}: {e}")
                return False
        return False

class ImageProcessor:
    """
    Provides utilities for processing image files.
    """
    THUMBNAIL_SIZE = (128, 128)
    _executor: Optional[ThreadPoolExecutor] = None

    @classmethod
    def get_executor(cls) -> ThreadPoolExecutor:
        """Get or create a thread pool executor for CPU-bound operations."""
        if cls._executor is None:
            cls._executor = ThreadPoolExecutor(max_workers=4)
        return cls._executor

    @classmethod
    async def get_image_info(cls, image_path: str) -> Dict:
        """
        Extracts width and height from an image file.

        Args:
            image_path: The path to the image file.

        Returns:
            A dictionary with the image's width and height.
        """
        def _get_image_info_sync(path: str) -> Dict:
            try:
                with Image.open(path) as img:
                    return {"width": img.width, "height": img.height}
            except Exception as e:
                raise Exception(f"Could not read image properties: {e}")

        try:
            # Run the synchronous PIL operation in a thread pool
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(cls.get_executor(), _get_image_info_sync, image_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    async def create_thumbnail(cls, image_path: str, thumbnail_path: str):
        """
        Creates a thumbnail for a given image.

        Args:
            image_path: The path to the source image.
            thumbnail_path: The path where the thumbnail will be saved.
        """
        def _create_thumbnail_sync(src_path: str, dest_path: str):
            try:
                Path(dest_path).parent.mkdir(exist_ok=True, parents=True)
                with Image.open(src_path) as img:
                    img.thumbnail(cls.THUMBNAIL_SIZE)
                    img.save(dest_path)
            except Exception as e:
                raise Exception(f"Could not create thumbnail: {e}")

        try:
            # Run the synchronous PIL operation in a thread pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(cls.get_executor(), _create_thumbnail_sync, image_path, thumbnail_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def shutdown_executor(cls):
        """Shutdown the thread pool executor. Call this on application shutdown."""
        if cls._executor:
            cls._executor.shutdown(wait=True)
            cls._executor = None
