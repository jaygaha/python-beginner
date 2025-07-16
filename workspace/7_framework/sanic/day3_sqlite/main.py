"""
App entrypoint.
"""
import logging
from app import app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Sanic Notes API server...")
    logger.info("Server will be available at http://0.0.0.0:8880")
    logger.info("Available endpoints:")
    logger.info("  GET  /api/search?q=<keyword> - Search functionality")
    logger.info("  GET  /api/square/<number> - Calculate square of number")
    logger.info("  POST /api/notes - Create a new note")
    logger.info("  GET  /api/notes - Get all notes")
    logger.info("  GET  /api/external-ip - Get external IP address")

    app.run(host="0.0.0.0", port=8880, debug=True)
