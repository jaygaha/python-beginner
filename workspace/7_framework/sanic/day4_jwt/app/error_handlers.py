"""
Basic global error handling.
"""
from sanic.exceptions import Unauthorized
from sanic.response import json

def register(app):
    @app.exception(Unauthorized)
    async def handle_auth_error(request, exception):
        return json({"error": str(exception)}, status=401)

    @app.exception(Exception)
    async def handle_any_error(request, exception):
        return json({"error": str(exception)}, status=500)
