"""
Centralized error handler setup.
"""
from sanic.exceptions import NotFound, InvalidUsage
from sanic.response import json
import logging

logger = logging.getLogger(__name__)

def register(app):
    @app.exception(NotFound)
    async def not_found(request, exception):
        logger.warning(f"Route not found: {request.path}")
        return json({"error": "Route not found", "path": request.path}, status=404)

    @app.exception(InvalidUsage)
    async def invalid_usage(request, exception):
        logger.warning(f"Invalid usage: {str(exception)} - Path: {request.path}")
        return json({"error": str(exception)}, status=400)

    @app.exception(Exception)
    async def server_error(request, exception):
        logger.error(f"Server error: {str(exception)} - Path: {request.path}", exc_info=True)
        return json({"error": "Internal server error"}, status=500)
