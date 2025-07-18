"""
Enable CORS + connect DB
"""
from sanic import Sanic
from sanic_ext import Extend
# from sanic_ext.extensions.cors import CORS
from app import db, auth
from sanic_cors import CORS

app = Sanic("SanicDay5App")

# Enable validation, injection, and CORS
Extend(app)

# Allow CORS for all origins
# app.ext.add_cors("*")
# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
CORS(app, resources=r'/api/*', origins="*", methods=["GET", "POST", "HEAD", "OPTIONS"])

# Connect/disconnect DB
@app.listener("before_server_start")
async def setup_db(app, loop):
    await db.connect()

@app.listener("after_server_stop")
async def close_db(app, loop):
    await db.disconnect()

# Middleware to protect JWT routes
app.middleware("request")(auth.auth_middleware)

from app import routes  # Required for route registration
