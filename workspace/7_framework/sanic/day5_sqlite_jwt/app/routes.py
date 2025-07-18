"""
Main routes — auth, file upload, notes
"""
import os
import uuid
import logging
from pathlib import Path
from sanic.response import json, file
from sanic.request import Request
from app import app, auth
from app import models

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logger = logging.getLogger(__name__)

# Allowed file extensions for security
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_user_input(username, password):
    """Validate username and password input"""
    if not username or not password:
        return False, "Username and password are required"
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not username.replace('_', '').replace('-', '').isalnum():
        return False, "Username can only contain letters, numbers, hyphens, and underscores"
    return True, None

def validate_note_content(content):
    """Validate note content"""
    if not content:
        return False, "Note content is required"
    if len(content) > 1000:
        return False, "Note content cannot exceed 1000 characters"
    return True, None

def is_allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """Generate a secure filename to prevent path traversal"""
    if not filename:
        return None
    # Get file extension
    ext = Path(filename).suffix.lower()
    # Generate unique filename
    return f"{uuid.uuid4().hex}{ext}"

@app.post("/api/register")
async def register(request: Request):
    if not request.json:
        return json({"error": "JSON body required"}, status=400)

    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validate input
    is_valid, error_msg = validate_user_input(username, password)
    if not is_valid:
        return json({"error": error_msg}, status=400)

    try:
        await models.create_user(username, password)
        return json({"message": "User registered"})
    except Exception:
        return json({"error": "Username already taken"}, status=409)

@app.post("/api/login")
async def login(request: Request):
    if not request.json:
        return json({"error": "JSON body required"}, status=400)

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return json({"error": "Username and password are required"}, status=400)

    user_id = await models.verify_user_password(username, password)
    if not user_id:
        return json({"error": "Invalid credentials"}, status=401)
    token = auth.create_token(user_id)
    return json({"token": token})

@app.post("/api/secure/notes")
async def add_note(request: Request):
    if not request.json:
        return json({"error": "JSON body required"}, status=400)

    data = request.json
    content = data.get("content")

    # Validate note content
    is_valid, error_msg = validate_note_content(content)
    if not is_valid:
        return json({"error": error_msg}, status=400)

    try:
        await models.add_note(content, request.ctx.user_id)
        return json({"message": "Note added"})
    except Exception:
        return json({"error": "Failed to add note"}, status=500)

@app.get("/api/secure/notes")
async def list_notes(request: Request):
    try:
        limit = int(request.args.get("limit", 5))
        offset = int(request.args.get("offset", 0))

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return json({"error": "Limit must be between 1 and 100"}, status=400)
        if offset < 0:
            return json({"error": "Offset must be non-negative"}, status=400)

        notes = await models.get_notes(request.ctx.user_id, limit, offset)
        return json({"notes": notes})
    except ValueError:
        return json({"error": "Invalid pagination parameters"}, status=400)
    except Exception:
        return json({"error": "Failed to fetch notes"}, status=500)

@app.post("/api/secure/upload")
async def upload(request: Request):
    if not request.files or "file" not in request.files:
        return json({"error": "No file uploaded"}, status=400)
    f = request.files.get("file")
    if not f or not f.name:
        return json({"error": "No file uploaded"}, status=400)

    # Check file size
    if len(f.body) > MAX_FILE_SIZE:
        return json({"error": "File too large"}, status=413)

    # Check file extension
    if not is_allowed_file(f.name):
        return json({"error": "File type not allowed"}, status=400)

    # Generate secure filename
    secure_name = secure_filename(f.name)
    if not secure_name:
        return json({"error": "Invalid filename"}, status=400)

    path = os.path.join(UPLOAD_FOLDER, secure_name)
    try:
        with open(path, "wb") as out:
            out.write(f.body)
        return json({"message": "File uploaded", "filename": secure_name, "original_name": f.name})
    except Exception as e:
        logger.error(f"Failed to save file {secure_name}: {e}")
        return json({"error": "Failed to save file"}, status=500)

@app.get("/api/secure/download/<filename>")
async def download(request: Request, filename: str):
    # Validate filename to prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return json({"error": "Invalid filename"}, status=400)

    path = os.path.join(UPLOAD_FOLDER, filename)
    # Ensure the path is within the upload folder
    if not os.path.abspath(path).startswith(os.path.abspath(UPLOAD_FOLDER)):
        return json({"error": "Invalid file path"}, status=400)

    if not os.path.exists(path):
        return json({"error": "File not found"}, status=404)
    return await file(path)
