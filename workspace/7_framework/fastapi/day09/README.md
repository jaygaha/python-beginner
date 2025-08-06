# FastAPI Day 09: Database Integration with SQLAlchemy

Welcome to **Day 09** of the FastAPI tutorial series! Building on the concepts from previous days, today we'll integrate a database into our application. You'll learn how to set up a connection, define data models, and perform CRUD (Create, Read, Update, Delete) operations using SQLAlchemy, the de facto standard for database interaction in the Python ecosystem.

---

## What You'll Learn

-   Connect a FastAPI application to a SQL database using SQLAlchemy.
-   Define database tables using SQLAlchemy's ORM (Object-Relational Mapper).
-   Manage database configuration securely using `.env` files and Pydantic settings.
-   Structure a database-driven application by separating concerns into modules.
-   Understand the critical difference between SQLAlchemy models and Pydantic schemas.
-   Implement a dependency injection system for managing database sessions.
-   Write unit tests for API endpoints that interact with a database.

---

## Key Concepts

### 1. Application Structure

Just as we separated file handling logic in Day 08, this project uses a modular structure to keep the codebase clean and maintainable.

-   `main.py`: The application's entry point. It initializes the FastAPI app, creates the database tables, and includes the feature-specific routers.
-   `database/`: A dedicated module for all database-related configuration and session management.
    -   `config.py`: Uses `pydantic-settings` to load the `DATABASE_URL` from the `.env` file. This avoids hardcoding sensitive credentials.
    -   `database.py`: Contains the core SQLAlchemy setup: the `engine`, the `SessionLocal` factory for creating sessions, and the declarative `Base` class that our ORM models will inherit from.
-   `newsletter/`: A module representing a single feature of our application (a newsletter subscription service).
    -   `models.py`: Defines the SQLAlchemy ORM models (e.g., `NewsletterSubscription`), which map to database tables.
    -   `schemas.py`: Defines the Pydantic models used for data validation and serialization in API requests and responses.
    -   `routes.py`: Contains the API endpoints (`/subscribe`, `/unsubscribe`, etc.).
    -   `utils.py`: Holds the business logic (the CRUD functions) that interacts with the database.
-   `tests/`: Contains unit tests for the API, now adapted to work with a test database.

### 2. Database Configuration (`database/config.py`)

We use `pydantic-settings` to manage configuration. This allows us to define our required environment variables in a Pydantic model. It automatically reads from an `.env` file, providing a robust way to configure the application without exposing secrets in the code.

```python-beginner/workspace/7_framework/fastapi/day09/database/config.py#L1-L8
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. Session Management and Dependency Injection (`database/database.py`)

Efficiently managing database connections is critical. This project uses FastAPI's dependency injection system to handle sessions:

-   **`engine`**: The central point of communication with the database.
-   **`SessionLocal`**: A factory that creates new database session objects.
-   **`get_db`**: A dependency function (and a generator) that creates a new session for each incoming request, passes it to the path operation function, and guarantees that the session is closed afterward, even if an error occurs.

```python-beginner/workspace/7_framework/fastapi/day09/database/database.py#L22-L28
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
This dependency is then injected into our route handlers, ensuring every request gets its own isolated session.

### 4. Models vs. Schemas: A Critical Distinction

This is one of the most important concepts when combining FastAPI and SQLAlchemy.

-   **SQLAlchemy Models (`newsletter/models.py`)**: These are Python classes that map to database tables. They define the table name and columns. They are the source of truth for your database structure and are used directly by your business logic (`utils.py`) to query and manipulate data.

    ```python-beginner/workspace/7_framework/fastapi/day09/newsletter/models.py#L5-L11
    class NewsletterSubscription(Base):
        __tablename__ = "newsletter_subscriptions"
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String(255) , unique=True , nullable=True)
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime, default=datetime.now)
    ```

-   **Pydantic Schemas (`newsletter/schemas.py`)**: These are Pydantic models that define the shape of the data for your API. They are used for request body validation and for formatting response data. By using schemas, you create a clear and secure API contract, preventing accidental exposure of database model fields that should not be sent to the client.

    ```python-beginner/workspace/7_framework/fastapi/day09/newsletter/schemas.py#L11-L18
    class NewsletterSubscriptionResponse(NewsletterSubscriptionBase):
        id: int
        is_active: bool
        created_at: datetime

        class Config:
            from_attributes = True
    ```
    The `Config.from_attributes = True` (formerly `orm_mode`) tells Pydantic to read the data from ORM model attributes, not just dictionaries.

### 5. Testing with a Database

Testing code that interacts with a database requires a special setup to ensure tests are isolated and don't interfere with each other or with the development database.

Our `tests/test_newsletter.py` demonstrates how to:
-   **Use a Test Database**: It creates an in-memory SQLite database for the duration of the test run.
-   **Override Dependencies**: It uses `app.dependency_overrides` to replace the main `get_db` dependency with one that connects to the test database.
-   **Use Fixtures for Setup/Teardown**: A `pytest` fixture is used to create the database schema before each test and tear it down afterward, ensuring every test starts with a clean slate.

---

## Next Steps

-   Examine the `.env` file and see how the `DATABASE_URL` is defined. Try changing it to a different SQLite file path.
-   Run the application with `uvicorn main:app --reload` and use an API client to test the `/newsletter/subscribe` and `/newsletter/subscriptions` endpoints.
-   Run the tests with `python -m pytest` to see the automated testing in action.
-   Trace the lifecycle of a request: follow a call from a function in `routes.py`, to the business logic in `utils.py`, and see how it uses the SQLAlchemy model from `models.py` and the Pydantic schema from `schemas.py`.

---