from sanic import Sanic
from sanic_ext import Extend
from app.routes import register_routes
from app.services import UserService, TodoService

app = Sanic("SanicTodoApp")

# Initialize Sanic-Ext once here
ext = Extend(app)

# Add dependencies
ext.add_dependency(UserService)
ext.add_dependency(TodoService)

# Register routes
register_routes(app)
