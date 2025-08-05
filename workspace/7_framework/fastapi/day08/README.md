# FastAPI Day 08: Advanced File Uploads and Static Files

Welcome to **Day 08** of the FastAPI tutorial! Today, you'll dive deep into handling file uploads, a crucial feature for many web applications. You'll learn how to manage single and multiple file uploads, perform server-side validation, and serve the uploaded files back to the user.

---

## What You'll Learn

-   Handle single, multiple, and metadata-rich file uploads.
-   Implement robust server-side validation for file size and type.
-   Store files on the server with a structured and secure approach.
-   Serve uploaded files statically using `StaticFiles`.
-   Process image files, including generating thumbnails.
-   Stream large files efficiently to reduce memory usage.
-   Structure a file-handling application by separating concerns.

---

## Key Concepts

### 1. Handling File Uploads with `UploadFile`

FastAPI makes handling uploaded files straightforward with the `UploadFile` class. Unlike a simple `bytes` object, `UploadFile` is a spooled file, which means it stores the file in memory up to a certain size limit and then spills it over to disk. This makes it efficient for both small and large files.

To use it, you declare a parameter in your path operation function with the `UploadFile` type hint and the `File()` dependency.

Example from `src/main.py`:
```python
# from src/main.py
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/single/")
async def upload_single_file(file: UploadFile = File(...)):
    # ... file processing logic ...
    return {"filename": file.filename, "content_type": file.content_type}
```
`UploadFile` has several useful attributes and async methods, including `filename`, `content_type`, `file` (the spooled file object), `read()`, and `seek()`.

### 2. Combining Files with Other Form Data

Often, you need to upload a file along with other data, like a description or a boolean flag. To do this, you use `Form()` for the other data fields. FastAPI understands that when `File()` and `Form()` are mixed, the request should be treated as `multipart/form-data`.

Example from `src/main.py`:
```python
# from src/main.py
from typing import Optional
from fastapi import Form

@app.post("/upload/image/")
async def upload_image(
    image: UploadFile = File(...),
    create_thumbnail: bool = Form(False),
    alt_text: Optional[str] = Form(None)
):
    # ... logic for handling the image and other form data ...
    return {"alt_text": alt_text, "thumbnail_created": create_thumbnail}
```

### 3. Server-Side Validation

Never trust user-provided files. It's critical to validate files on the server to ensure they meet your application's requirements for size and type. This prevents users from uploading excessively large files that could overwhelm your server or malicious files disguised with a harmless extension.

In our project, the `FileValidator` class in `file_handlers.py` handles this logic.

Example from `src/file_handlers.py`:
```python
# from src/file_handlers.py
from fastapi import UploadFile, HTTPException, status

class FileValidator:
    ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

    @classmethod
    async def validate_file(cls, file: UploadFile, file_type: str = "any"):
        if file.size > cls.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File is too large."
            )
        if file_type == "image" and file.content_type not in cls.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image type."
            )
        return True
```

### 4. File Storage and Organization

Storing files with their original filenames can lead to conflicts if two users upload a file with the same name. A common strategy is to generate a unique filename (e.g., using `uuid.uuid4()`) and store the original filename in a database for later retrieval.

This project also organizes files into category-based subdirectories (`images/`, `documents/`, etc.) within a main `uploads` directory. This separation makes the file system easier to manage.

### 5. Serving Static Files with `StaticFiles`

Once a file is uploaded, you need a way to serve it back to users. FastAPI uses `StaticFiles` to mount a directory, making all of its contents available at a specified URL path.

Example from `src/main.py`:
```python
# from src/main.py
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="uploads"), name="static")
```
With this configuration, a file saved at `uploads/images/my-file.png` can be accessed by clients at the URL `http://localhost:8000/static/images/my-file.png`.

### 6. Application Structure

This project separates concerns into different modules, which is a best practice for building maintainable applications:
-   `main.py`: Contains the FastAPI app instance and all API endpoint definitions. It handles the "what" (the routes).
-   `file_handlers.py`: Contains the business logic for file validation, storage, and processing. It handles the "how" (the implementation details).
-   `models.py`: Defines the Pydantic models used for request validation and response serialization. It defines the data shapes.
-   `tests/`: Contains unit and integration tests to ensure the application works correctly.

---

## Next Steps

-   Explore the different upload endpoints in `src/main.py` (`/upload/single/`, `/upload/image/`, `/upload/multiple/`).
-   Review the logic in `FileStorage` and `ImageProcessor` in `src/file_handlers.py` to understand how files are saved and manipulated.
-   Run the application and use an API client like Postman or Insomnia to test the file upload endpoints. Try uploading valid and invalid files to see the validation in action.
-   After uploading a file, try accessing its `file_url` in your browser to see `StaticFiles` at work.
-   Examine the tests in `tests/test_main.py` to see how file uploads are tested programmatically.

---

**Tip:** For production applications, consider using a cloud storage service like Amazon S3, Google Cloud Storage, or Azure Blob Storage instead of the local file system. This provides better scalability, durability, and security.

---