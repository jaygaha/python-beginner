from sanic import Sanic

# Create a Sanic app instance
app = Sanic("SanicBasicApp")

# Import routes module
from app import routes
