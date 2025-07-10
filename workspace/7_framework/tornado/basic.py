import asyncio
import logging
import signal

import tornado.ioloop
import tornado.web
import os

# --- Configuration ---
# Grouping settings together makes them easier to manage.
SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,  # Enable auto-reloading and detailed error pages
}
PORT = 8888

# --- Request Handlers ---
# Using `async def` for all handlers is the modern standard for consistency.

class MainHandler(tornado.web.RequestHandler):
    """A simple handler for the root URL."""
    async def get(self) -> None:
        self.write("Hello, Modern Tornado World!")

class GreetHandler(tornado.web.RequestHandler):
    """Handles URL with parameters and renders a template."""
    async def get(self, name: str) -> None:
        # Assumes a 'hello.html' exists in the 'templates' directory.
        # Example: <h1>Hello, {{ name }}!</h1>
        self.render("hello.html", name=name)

class AsyncHandler(tornado.web.RequestHandler):
    """Demonstrates a non-blocking, asynchronous operation."""
    async def get(self) -> None:
        await asyncio.sleep(1)
        self.write("Async operation completed!")

# --- URL Routing ---
# Centralizing URL patterns makes them easy to find and update.
def make_app() -> tornado.web.Application:
    """Creates and returns the Tornado application instance."""
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/hello/([^/]+)", GreetHandler), # More specific regex
        (r"/async", AsyncHandler),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {"path": SETTINGS["static_path"]},
        ),
    ], **SETTINGS)

# --- Graceful Shutdown ---
# This approach is more robust and integrated with Tornado's event loop.
def sig_handler(sig: int, frame) -> None:
    """Signal handler to initiate a graceful shutdown."""
    logging.info(f"Caught signal: {sig}. Shutting down...")
    ioloop = tornado.ioloop.IOLoop.current()
    # Add a callback to stop the IOLoop on the next iteration
    ioloop.add_callback_from_signal(ioloop.stop)

# --- Application Runner ---
async def main() -> None:
    """The main entry point for the application."""
    app = make_app()
    app.listen(PORT)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, sig_handler)  # Catches Ctrl+C
    signal.signal(signal.SIGTERM, sig_handler) # Catches `kill` command

    logging.info(f"Server is running at http://localhost:{PORT}")
    logging.info("Press Ctrl+C to stop")

    # This keeps the main coroutine running until the IOLoop is stopped.
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutdown complete.")
