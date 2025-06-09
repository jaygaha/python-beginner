from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from .models import Base, DBSession


def setup_session(config):
    """Configure session management and CSRF protection."""
    session_factory = SignedCookieSessionFactory("itsaseekreet")
    config.set_session_factory(session_factory)
    # Use default CSRF settings - protection enabled per view basis
    config.set_default_csrf_options(require_csrf=False)


def setup_database(config):
    """Configure the database engine and bind the session."""
    settings = config.get_settings()
    # Add SQLite threading configuration
    if 'sqlite' in settings.get('sqlalchemy.url', ''):
        from sqlalchemy.pool import StaticPool
        settings['sqlalchemy.connect_args'] = {'check_same_thread': False}
        settings['sqlalchemy.poolclass'] = StaticPool
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    # For dev only: create tables automatically
    Base.metadata.create_all(engine)


def setup_routes(config):
    """Configure application routes."""
    config.add_static_view(name="static", path="tasks:static")
    config.add_route("tasks", "/")
    config.add_route("task_add", "/tasks/add")
    config.add_route("task", "/tasks/{id}")


def create_app(global_config, **settings):
    """
    Create and configure the Pyramid WSGI application.

    Returns:
        A configured WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Include necessary Pyramid packages
        config.include("pyramid_tm")
        config.include("pyramid_jinja2")

        # Configure Jinja2 template directory
        config.add_jinja2_search_path("tasks:templates")

        # Set up core components
        setup_session(config)
        setup_database(config)
        setup_routes(config)

        # Scan for views and other configuration decorators
        config.scan(".views")

        return config.make_wsgi_app()
