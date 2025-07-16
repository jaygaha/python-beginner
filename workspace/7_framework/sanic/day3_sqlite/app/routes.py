"""
Routes for the notes application.
"""
from sanic.response import json
from sanic.exceptions import InvalidUsage
from app import app, database
import httpx
import logging

logger = logging.getLogger(__name__)

# Query parameters
@app.route("/api/search")
async def search(request):
    keyword = request.args.get("q", None)
    if not keyword:
        return json({"error": "Missing query parameter 'q'"}, status=400)

    return json({"result": f"You searched for: {keyword}"})

# Typed URL parameter
@app.route("/api/square/<number:int>")
async def square(request, number):
    return json({"number": number, "square": number ** 2})

# JSON Validation
@app.post("/api/notes")
async def create_note(request):
    try:
        data = await request.json()
    except Exception:
        raise InvalidUsage("Invalid JSON in request body")

    if not data or "content" not in data:
        raise InvalidUsage("Missing 'content' in request body")

    content = data.get("content", "").strip()
    if not content:
        raise InvalidUsage("Content cannot be empty")

    await database.add_note(content)

    return json({"message": "Note added!", "content": content})

@app.route("/api/notes")
async def get_notes(request):
    notes = await database.get_notes()

    return json({"notes": notes})

# Async HTTP client call
@app.route("/api/external-ip")
async def external_ip(request):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://httpbin.org/ip")
            response.raise_for_status()  # Raise exception for bad status codes
            data = response.json()

        logger.info(f"External IP request successful: {data.get('origin', 'Unknown')}")
        return json({"your_ip": data["origin"]})

    except httpx.TimeoutException:
        logger.error("Timeout when requesting external IP")
        return json({"error": "Request timeout"}, status=504)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error when requesting external IP: {e}")
        return json({"error": "External service error"}, status=502)
    except Exception as e:
        logger.error(f"Unexpected error when requesting external IP: {e}")
        return json({"error": "Service unavailable"}, status=503)
