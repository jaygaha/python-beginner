# What is FastAPI?

**FastAPI** is a modern, high-performance web framework for building APIs with Python 3.7+, based on standard Python type hints. It's designed to be easy to use, fast to code, and production-ready.

## Key Features:

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase feature development speed by about 200% to 300%
- **Fewer bugs**: Reduce about 40% of human-induced errors
- **Intuitive**: Great editor support with auto-completion
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Get production-ready code with automatic interactive documentation

## Environment Setup

**Create Project Folder**
```bash
mkdir my_fastapi_project
cd my_fastapi_project
```
**Initialize Project**
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
**Install Dependencies**
```bash
pip install fastapi uvicorn
```
- `fastapi`: The web framework for building APIs with Python.
- `uvicorn`: The ASGI server for running FastAPI applications.

## Creating Your First API

Create `main.py`
```python
from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Running Your First API

**Run using uvicorn with `--reload` for auto-reloading**
```
uvicorn main:app --reload
```

## Tutorials

- [Day 01: FastAPI Basics & Testing](day01/README.md)
  Learn how to build your first FastAPI application, create simple endpoints, and write automated tests.
  _Includes: project structure, endpoint examples, running instructions, and test coverage._

- [Day 02: Request & Response Models, Validation, and Testing](day02/README.md)
  Learn how to define request and response models with Pydantic, validate user input, build basic CRUD endpoints, and write automated tests for your API.
  _Includes: user model examples, validation, CRUD routes, and test coverage._

- [Day 03: Path Parameters and Query Parameters](day03/README.md)
  Learn how to handle user requests with path parameters and query parameters. This includes validation, filtering, sorting, and automated tests.
  _Includes: path parameter examples, query parameter examples, and test coverage._

---

## Recommended Project Structure

```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py  # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```
