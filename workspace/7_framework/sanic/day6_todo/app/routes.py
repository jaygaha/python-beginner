from sanic import Request, HTTPResponse
from sanic.response import json

from app.services import UserService, TodoService

def register_routes(app):
    @app.get("/users")
    async def list_users(request: Request, user_service: UserService) -> HTTPResponse:
        users = user_service.get_users()
        return json({"users": users})

    @app.get("/user")
    async def get_user(request: Request, user_service: UserService) -> HTTPResponse:
        user_id_str = request.args.get("id")
        if not user_id_str:
            return json({"error": "User ID is required"}, status=400)

        try:
            user_id = int(user_id_str)
        except ValueError:
            return json({"error": "User ID must be a valid integer"}, status=400)

        user = user_service.get_user(user_id)
        if user:
            return json({"user": user})
        return json({"error": "User not found"}, status=404)

    # Todo routes
    @app.get("/todos")
    async def list_todos(request: Request, todo_service: TodoService) -> HTTPResponse:
        user_id_str = request.args.get("user_id")
        user_id = None

        if user_id_str:
            try:
                user_id = int(user_id_str)
            except ValueError:
                return json({"error": "User ID must be a valid integer"}, status=400)

        todos = todo_service.get_todos(user_id)
        return json({"todos": todos})

    @app.post("/todo")
    async def create_todo(request: Request, todo_service: TodoService) -> HTTPResponse:
        if not request.json:
            return json({"error": "JSON body is required"}, status=400)

        title = request.json.get("title")
        description = request.json.get("description")
        user_id_value = request.json.get("user_id")

        if not title or not description or user_id_value is None:
            return json({"error": "Title, description, and user_id are required"}, status=400)

        if not isinstance(title, str) or not isinstance(description, str):
            return json({"error": "Title and description must be strings"}, status=400)

        try:
            user_id = int(user_id_value)
        except (ValueError, TypeError):
            return json({"error": "User ID must be a valid integer"}, status=400)

        todo = todo_service.create_todo(title, description, user_id)
        return json({"todo": todo}, status=201)

    @app.get("/todos/<todo_id:int>")
    async def get_todo(request: Request, todo_service: TodoService, todo_id: int) -> HTTPResponse:
        todo = todo_service.get_todo(todo_id)
        if todo:
            return json({"todo": todo})
        return json({"error": "Todo not found"}, status=404)

    @app.put("/todo")
    async def update_todo(request: Request, todo_service: TodoService) -> HTTPResponse:
        if not request.json:
            return json({"error": "JSON body is required"}, status=400)

        todo_id_str = request.args.get("id")
        if not todo_id_str:
            return json({"error": "Todo ID is required in query parameters"}, status=400)

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            return json({"error": "Todo ID must be a valid integer"}, status=400)

        title = request.json.get("title")
        description = request.json.get("description")
        completed = request.json.get("completed", False)  # Default to False if not provided

        if not title or not description:
            return json({"error": "Title and description are required"}, status=400)

        if not isinstance(title, str) or not isinstance(description, str):
            return json({"error": "Title and description must be strings"}, status=400)

        if not isinstance(completed, bool):
            return json({"error": "Completed must be a boolean"}, status=400)

        todo = todo_service.update_todo(todo_id, title, description, completed)
        if todo:
            return json({"todo": todo})
        return json({"error": "Todo not found"}, status=404)

    @app.delete("/todo")
    async def delete_todo(request: Request, todo_service: TodoService) -> HTTPResponse:
        todo_id_str = request.args.get("id")
        if not todo_id_str:
            return json({"error": "Todo ID is required"}, status=400)

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            return json({"error": "Todo ID must be a valid integer"}, status=400)

        success = todo_service.delete_todo(todo_id)
        if success:
            return json({"message": "Todo deleted successfully"})
        return json({"error": "Todo not found"}, status=404)

    @app.patch("/todo/<todo_id:int>/toggle")
    async def toggle_todo_completion(request: Request, todo_service: TodoService, todo_id: int) -> HTTPResponse:
        todo = todo_service.toggle_todo_completion(todo_id)
        if todo:
            return json({"todo": todo})
        return json({"error": "Todo not found"}, status=404)
