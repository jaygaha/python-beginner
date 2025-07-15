"""
Basic standalone routes (if needed outside blueprints)
"""
from sanic.response import text
from app import app

@app.route("/")
async def home(request):
    return text("Hello, Sanic World!")
