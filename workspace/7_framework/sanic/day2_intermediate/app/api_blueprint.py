"""
Create a Blueprint to logically group API routes.
"""
from sanic import Blueprint
from sanic.response import json

api = Blueprint("api", url_prefix="/api")

@api.route("/status")
async def status(request):
    return json({"status": "running"})

@api.route("/user/<name>")
async def greet_user(request, name):
    return json({"message": f"Hello, {name}!"})
