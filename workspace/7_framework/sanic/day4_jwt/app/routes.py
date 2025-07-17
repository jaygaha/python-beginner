"""
All routes with validation and secure access.
"""
from sanic_ext import validate
from sanic.response import json
from sanic import Request
from app import app, auth
from app.schema import LoginRequest, NoteCreateRequest

# Fake user store
users = {"jay": {"password": "secret", "id": 1}}

notes = []

@app.post("api/login")
@validate(json=LoginRequest)
async def login(request: Request, body: LoginRequest):
    user = users.get(body.username)
    if not user or user["password"] != body.password:
        return json({"error": "Invalid credentials"}, status=401)
    token = auth.create_token(user["id"])
    return json({"token": token})

@app.post("/api/secure/notes")
@validate(json=NoteCreateRequest)
async def create_note(request: Request, body: NoteCreateRequest):
    notes.append({"user": request.ctx.user, "content": body.content})
    return json({"message": "Note added!"})

@app.get("/api/secure/notes")
async def list_notes(request: Request):
    user_notes = [n for n in notes if n["user"] == request.ctx.user]
    return json({"notes": user_notes})
