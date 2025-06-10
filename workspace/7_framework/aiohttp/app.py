from aiohttp import web
from notes_handler import (create_note_handler, get_all_notes_handler, get_note_handler,
                           update_note_handler, delete_note_handler)
from default_handler import index_handler

app = web.Application()

# Route definations
app.router.add_get('/notes', get_all_notes_handler)
app.router.add_get('/notes/{id}', get_note_handler)
app.router.add_post('/notes', create_note_handler)
app.router.add_put('/notes/{id}', update_note_handler)
app.router.add_delete('/notes/{id}', delete_note_handler)
app.router.add_get('/', index_handler)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8070)
