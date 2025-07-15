"""
Centralized error handling setup.
"""
from sanic.exceptions import NotFound
from sanic.response import json

def register(app):
    @app.exception(NotFound)
    async def not_found(request, exception):
        return json({"error": "Route not found!"}, status=404)

    @app.exception(Exception)
    async def server_error(request, exception):
        return json({"error": str(exception)}, status=500)
