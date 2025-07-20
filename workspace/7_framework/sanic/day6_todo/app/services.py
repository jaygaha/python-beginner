from app.types import Todo, User

class UserService:
    def __init__(self):
        self.users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]

    def get_user(self, user_id: int) -> User | None:
        """Get a single user by ID"""
        user_dict = next((user for user in self.users if user["id"] == user_id), None)
        if user_dict is None:
            return None
        return User(**user_dict)

    def get_users(self) -> list[User]:
        """Get all users"""
        return [User(**user) for user in self.users]

class TodoService:
    def __init__(self):
        self.todos = [
            {
                "id": 1,
                "title": "Learn Python",
                "description": "Master the basics of Python programming",
                "completed": False,
                "user_id": 1
            },
            {
                "id": 2,
                "title": "Build a Todo App",
                "description": "Create a simple Todo app using Sanic",
                "completed": False,
                "user_id": 1
            }
        ]
        self.next_id = 3  # Track next available ID

    def create_todo(self, title: str, description: str, user_id: int) -> Todo:
        """Create a new todo item"""
        new_todo = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "completed": False,
            "user_id": user_id
        }
        self.todos.append(new_todo)
        self.next_id += 1
        return Todo(**new_todo)

    def get_todo(self, todo_id: int) -> Todo | None:
        """Get a single todo by ID"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                return Todo(**todo)
        return None

    def get_todos(self, user_id: int | None = None) -> list[Todo]:
        """Get todos, optionally filtered by user_id"""
        if user_id is None:
            # Return all todos if no user_id specified
            return [Todo(**todo) for todo in self.todos]
        else:
            # Return todos for specific user
            return [Todo(**todo) for todo in self.todos if todo["user_id"] == user_id]

    def update_todo(self, todo_id: int, title: str, description: str, completed: bool) -> Todo | None:
        """Update an existing todo item"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                # Create updated todo
                updated_todo = {
                    "id": todo_id,
                    "title": title,
                    "description": description,
                    "completed": completed,
                    "user_id": todo["user_id"]  # Keep original user_id
                }
                # Replace the old todo with updated one
                self.todos[i] = updated_todo
                return Todo(**updated_todo)
        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item by ID"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                self.todos.pop(i)
                return True
        return False

    def toggle_todo_completion(self, todo_id: int) -> Todo | None:
        """Toggle the completion status of a todo"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                updated_todo = todo.copy()
                updated_todo["completed"] = not updated_todo["completed"]
                self.todos[i] = updated_todo
                return Todo(**updated_todo)
        return None
