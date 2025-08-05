from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileUploadResponse(BaseModel):
    id: str
    original_filename: str
    saved_filename: str
    file_size: int
    content_type: str
    file_hash: str
    upload_timestamp: datetime
    file_url: str

class ImageUploadResponse(FileUploadResponse):
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail_url: Optional[str] = None

class FileMetadata(BaseModel):
    filename: str
    size: int
    content_type: str
    upload_date: datetime
    uploader: Optional[str] = None

class BatchUploadResponse(BaseModel):
    successful_uploads: List[FileUploadResponse]
    failed_uploads: List[dict]
    total_files: int
    success_count: int
    failure_count: int

class SearchRequest(BaseModel):
    query: str
    content_types: Optional[List[str]] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
