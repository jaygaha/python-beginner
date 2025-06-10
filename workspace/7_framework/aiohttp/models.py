import uuid
from datetime import datetime

# in-memory storage for notes
notes = {}


# Helper to create a new note
def create_note(title, content):
    note_id = str(uuid.uuid4())
    nowTime = datetime.now()
    note = {
        'id': note_id,
        'title': title,
        'content': content,
        'updated_at': nowTime.isoformat(),
        'created_at': nowTime.isoformat()
    }

    notes[note_id] = note
    return note


# Fetch all notes
def fetch_all_notes():
    return list(notes.values())


# Get a single note by id
def fetch_note(note_id):
    return notes.get(note_id)


# Update a notes
def update_note(note_id, title, content):
    note = notes.get(note_id)
    nowTime = datetime.now()
    if note:
        note['title'] = title
        note['content'] = content
        note['updated_at'] = nowTime.isoformat()

        return note

    return None


# Delete a note by id
def delete_note(note_id):
    return notes.pop(note_id, None)
