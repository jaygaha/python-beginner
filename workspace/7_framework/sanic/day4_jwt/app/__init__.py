from sanic import Sanic
from sanic_ext import Extend
from app import error_handlers, auth

app = Sanic("SanicJWT")

# Enable sanic-ext features (validations, DI, caching, logging, security, etc)
Extend(app)

# Register global exception handler
error_handlers.register(app)

# Add authentication routes
app.middleware("request")(auth.auth_middleware)

from app import routes
