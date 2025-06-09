from wsgiref.simple_server import make_server
from tasks import create_app


def main():
    """Initialize and run the Pyramid task management application."""
    global_config = {}
    settings = {
        'sqlalchemy.url': 'sqlite:///tasks.db'  # or your config here
    }

    app = create_app(global_config, **settings)

    server = make_server("0.0.0.0", 6543, app)
    print("Serving on http://localhost:6543...")
    server.serve_forever()


if __name__ == "__main__":
    main()
