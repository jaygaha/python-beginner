"""
Initialize the app, error handlers, and database connection.
"""
import logging
from sanic import Sanic
from app import error_handlers, database
from app.config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.logging.level),
    format=config.logging.format
)
logger = logging.getLogger(__name__)

app = Sanic("SanicDBApp")

error_handlers.register(app)

@app.listener("before_server_start")
async def setup_db(app, loop):
    logger.info("Setting up database connection...")
    await database.connect()

@app.listener("before_server_stop")
async def teardown_db(app, loop):
    logger.info("Closing database connection...")
    await database.disconnect()

from app import routes
