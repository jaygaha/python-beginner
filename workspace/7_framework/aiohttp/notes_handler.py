from aiohttp import web
from models import create_note, fetch_all_notes, fetch_note, update_note, delete_note


# Create a new note
async def create_note_handler(request):
    data = await request.json()
    title = data.get("title")
    content = data.get("content")

    # validate input data
    if not title or not content:
        return web.json_response({"error": "Title and content are required"}, status=400)

    note = create_note(title, content)

    return web.json_response(note, status=201)


# Get all notes
async def get_all_notes_handler(request):
    return web.json_response(fetch_all_notes())


# Get a single note
async def get_note_handler(request):
    note_id = request.match_info.get("id")
    note = fetch_note(note_id)

    if not note:
        return web.json_response({"error": "Note not found"}, status=404)
    return web.json_response(note)


# Update a note
async def update_note_handler(request):
    note_id = request.match_info.get("id")
    data = await request.json()
    title = data.get("title")
    content = data.get("content")

    # validation
    if not title or not content:
        return web.json_response({"error": "Title and content are required"}, status=400)

    updated = update_note(note_id, title, content)

    if updated:
        return web.json_response(updated)
    else:
        return web.json_response({"error": "Note not found"}, status=404)


# Delete a note
async def delete_note_handler(request):
    note_id = request.match_info.get("id")
    deleted = delete_note(note_id)

    if deleted:
        return web.json_response({"message": "Note deleted successfully"}, status=200)
    else:
        return web.json_response({"error": "Note not found"}, status=404)
