"""
Define request validation schemas (like Pydantic but for Sanic).
"""
from dataclasses import dataclass

@dataclass
class LoginRequest:
    username: str
    password: str

@dataclass
class NoteCreateRequest:
    title: str
    content: str
