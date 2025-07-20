"""
model
"""
from typing import TypedDict

class User(TypedDict):
    id: int
    email: str
    name: str

class Todo(TypedDict):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int
