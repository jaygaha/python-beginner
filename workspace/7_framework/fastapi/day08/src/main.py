from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from file_handlers import FileValidator, FileStorage, ImageProcessor
from models import FileUploadResponse, ImageUploadResponse, BatchUploadResponse, FileMetadata, SearchRequest
from typing import List, Optional
import uuid
from datetime import datetime
from pathlib import Path
import aiofiles

app = FastAPI(title="File Upload API", version="1.0.0")

# Initialize file storage
file_storage = FileStorage("uploads")

# Mount static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# In-memory file database (in production, use a real database)
files_db = {}

@app.post("/upload/single/", response_model=FileUploadResponse)
async def upload_single_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    # Validate file
    await FileValidator.validate_file(file)

    # Save file
    file_info = await file_storage.save_file(file, "general")

    # Create file record
    file_id = str(uuid.uuid4())
    file_record = {
        "id": file_id,
        "original_filename": file_info["original_filename"],
        "saved_filename": file_info["saved_filename"],
        "file_size": file_info["file_size"],
        "content_type": file_info["content_type"],
        "file_hash": file_info["file_hash"],
        "upload_timestamp": datetime.now(),
        "file_url": f"/static/general/{file_info['saved_filename']}",
        "description": description
    }

    files_db[file_id] = file_record

    return FileUploadResponse(**file_record)

@app.post("/upload/image/", response_model=ImageUploadResponse)
async def upload_image(
    image: UploadFile = File(...),
    create_thumbnail: bool = Form(False),
    alt_text: Optional[str] = Form(None)
):
    # Validate image
    await FileValidator.validate_file(image, "image")

    # Save image
    file_info = await file_storage.save_file(image, "images")
    image_path = file_info["file_path"]

    # Get image information
    image_info = await ImageProcessor.get_image_info(image_path)

    # Create thumbnail if requested
    thumbnail_url = None
    if create_thumbnail:
        thumbnail_filename = f"thumb_{file_info['saved_filename']}"
        thumbnail_path = file_storage.get_file_path(thumbnail_filename, "thumbnails")
        await ImageProcessor.create_thumbnail(image_path, str(thumbnail_path))
        thumbnail_url = f"/static/thumbnails/{thumbnail_filename}"

    # Create file record
    file_id = str(uuid.uuid4())
    file_record = {
        "id": file_id,
        "original_filename": file_info["original_filename"],
        "saved_filename": file_info["saved_filename"],
        "file_size": file_info["file_size"],
        "content_type": file_info["content_type"],
        "file_hash": file_info["file_hash"],
        "upload_timestamp": datetime.now(),
        "file_url": f"/static/images/{file_info['saved_filename']}",
        "width": image_info["width"],
        "height": image_info["height"],
        "thumbnail_url": thumbnail_url,
        "alt_text": alt_text
    }

    files_db[file_id] = file_record

    return ImageUploadResponse(**file_record)

@app.post("/upload/multiple/", response_model=BatchUploadResponse)
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    category: str = Form("general")
):
    successful_uploads = []
    failed_uploads = []

    for file in files:
        try:
            # Validate file
            await FileValidator.validate_file(file)

            # Save file
            file_info = await file_storage.save_file(file, category)

            # Create file record
            file_id = str(uuid.uuid4())
            file_record = {
                "id": file_id,
                "original_filename": file_info["original_filename"],
                "saved_filename": file_info["saved_filename"],
                "file_size": file_info["file_size"],
                "content_type": file_info["content_type"],
                "file_hash": file_info["file_hash"],
                "upload_timestamp": datetime.now(),
                "file_url": f"/static/{category}/{file_info['saved_filename']}"
            }

            files_db[file_id] = file_record
            successful_uploads.append(FileUploadResponse(**file_record))

        except Exception as e:
            failed_uploads.append({
                "filename": file.filename,
                "error": str(e)
            })

    return BatchUploadResponse(
        successful_uploads=successful_uploads,
        failed_uploads=failed_uploads,
        total_files=len(files),
        success_count=len(successful_uploads),
        failure_count=len(failed_uploads)
    )

@app.post("/upload/document/", response_model=FileUploadResponse)
async def upload_document(
    document: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form("documents")
):
    # Validate document
    await FileValidator.validate_file(document, "document")

    # Save document
    file_info = await file_storage.save_file(document, category)

    # Create file record
    file_id = str(uuid.uuid4())
    file_record = {
        "id": file_id,
        "original_filename": file_info["original_filename"],
        "saved_filename": file_info["saved_filename"],
        "file_size": file_info["file_size"],
        "content_type": file_info["content_type"],
        "file_hash": file_info["file_hash"],
        "upload_timestamp": datetime.now(),
        "file_url": f"/static/{category}/{file_info['saved_filename']}",
        "title": title,
        "category": category
    }

    files_db[file_id] = file_record

    return FileUploadResponse(**file_record)

@app.get("/files/", response_model=List[FileUploadResponse])
async def list_files(
    category: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = 50
):
    files = list(files_db.values())

    if category:
        files = [f for f in files if f.get("category") == category]

    if content_type:
        files = [f for f in files if f["content_type"] == content_type]

    return files[:limit]

@app.get("/files/{file_id}", response_model=FileUploadResponse)
async def get_file_info(file_id: str):
    file_record = files_db.get(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    return FileUploadResponse(**file_record)

@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    file_record = files_db.get(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Construct file path
    category = file_record.get("category", "general")
    file_path = file_storage.get_file_path(file_record["saved_filename"], category)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=file_record["original_filename"],
        media_type=file_record["content_type"]
    )

@app.get("/files/{file_id}/stream")
async def stream_file(file_id: str):
    file_record = files_db.get(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    category = file_record.get("category", "general")
    file_path = file_storage.get_file_path(file_record["saved_filename"], category)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    async def file_generator():
        async with aiofiles.open(file_path, mode='rb') as file:
            while chunk := await file.read(1024):  # Read in 1KB chunks
                yield chunk

    return StreamingResponse(
        file_generator(),
        media_type=file_record["content_type"],
        headers={"Content-Disposition": f"inline; filename={file_record['original_filename']}"}
    )

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    file_record = files_db.get(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete from disk
    category = file_record.get("category", "general")
    file_path = file_storage.get_file_path(file_record["saved_filename"], category)
    success = await file_storage.delete_file(str(file_path))

    # Delete thumbnail if exists
    if file_record.get("thumbnail_url"):
        thumbnail_filename = f"thumb_{file_record['saved_filename']}"
        thumbnail_path = file_storage.get_file_path(thumbnail_filename, "thumbnails")
        await file_storage.delete_file(str(thumbnail_path))

    # Delete from database
    del files_db[file_id]

    return {"message": "File deleted successfully", "deleted_from_disk": success}

@app.get("/files/{file_id}/metadata")
async def get_file_metadata(file_id: str):
    file_record = files_db.get(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    category = file_record.get("category", "general")
    file_path = file_storage.get_file_path(file_record["saved_filename"], category)

    metadata = {
        "file_exists": file_path.exists(),
        "file_size_on_disk": file_path.stat().st_size if file_path.exists() else 0,
        "recorded_size": file_record["file_size"],
        "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime) if file_path.exists() else None,
        "content_type": file_record["content_type"],
        "file_hash": file_record["file_hash"]
    }

    # Additional metadata for images
    if file_record["content_type"].startswith("image/") and file_path.exists():
        try:
            image_info = await ImageProcessor.get_image_info(str(file_path))
            metadata.update(image_info)
        except:
            pass

    return metadata

@app.post("/files/search")
async def search_files(search_request: SearchRequest):
    results = []

    for file_record in files_db.values():
        # Search in filename
        if search_request.query.lower() in file_record["original_filename"].lower():
            # Apply filters
            if search_request.content_types and file_record["content_type"] not in search_request.content_types:
                continue

            if search_request.min_size is not None and file_record["file_size"] < search_request.min_size:
                continue

            if search_request.max_size is not None and file_record["file_size"] > search_request.max_size:
                continue

            results.append(file_record)

    return {"query": search_request.query, "results": results, "count": len(results)}

# Health check
@app.get("/health")
async def health_check():
    upload_dir = Path("uploads")
    return {
        "status": "healthy",
        "upload_directory_exists": upload_dir.exists(),
        "total_files": len(files_db),
        "storage_subdirectories": [d.name for d in upload_dir.iterdir() if d.is_dir()] if upload_dir.exists() else []
    }
