from sanic.response import text, json
from app import app
import asyncio

# Home route
@app.route("/")
async def home(request):
    return text("Hello, Sanic world!")

# JSON response route
@app.route("/api/greet")
async def greet(request):
    return json({"message": "Hello, Sanic API!"})

# Route with URL parameter
@app.route("/api/user/<name>")
async def user(request, name):
    return json({"message": f"Hello, user {name}!"})

# Handle POST request
@app.route("/api/user", methods=["POST"])
async def create_user(request):
    data = await request.json()
    name = data.get("name")
    return json({"message": f"User {name} created!"})

# Async demo route
# Async demo route
@app.route("/api/wait")
async def wait(request):
    await asyncio.sleep(2)
    return json({"message": "Async demo completed! Waited for 2 seconds asynchronously!"})
