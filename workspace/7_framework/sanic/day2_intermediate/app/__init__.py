"""
App initialization with middleware, error handlers, listeners, and blueprints.
"""
from sanic import Sanic
from app import error_handlers, api_blueprint

# Create Sanic app instance
app = Sanic("SanicIntermediateApp")

# Register error handlers
error_handlers.register(app)

# Register API blueprint
app.blueprint(api_blueprint.api)

# Middleware example
@app.middleware("request")
async def print_request(request):
    print(f"Request: {request.method} {request.path}")

@app.middleware("response")
async def add_custom_header(request, response):
    response.headers["X-Powered-By"] = "Sanic Tutorial"

# Lifecycle event: after server stops
@app.listener("after_server_stop")
async def shutdown(app, loop):
    print("Server stopped, cleaning up resources.")
