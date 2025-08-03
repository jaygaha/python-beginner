# FastAPI Day 07: Middleware and CORS

Welcome to **Day 07** of the FastAPI tutorial! Today, you'll learn how to use middleware to intercept and process requests and responses, and how to configure Cross-Origin Resource Sharing (CORS) to allow your frontend applications to communicate with your API.

---

## What You'll Learn

-   Understand what middleware is and how it processes requests and responses.
-   Implement custom middleware for logging, performance monitoring, and adding custom headers.
-   Understand the importance of Cross-Origin Resource Sharing (CORS) for web applications.
-   Configure CORS middleware to securely allow frontend clients to access your API.
-   See how middleware is added to a FastAPI application and how the order matters.

---

## Key Concepts

### 1. What is Middleware?

**Middleware** is a function that works with every request before it is processed by a specific path operation and with every response before it is returned. It acts as a processing layer that can inspect, modify, or even block requests and responses.

Think of it like an onion with layers. A request travels inward through each layer of middleware to the application's core, and the response travels outward through the same layers in reverse order.

In FastAPI, you create middleware using the `@app.middleware("http")` decorator.

### 2. Implementing Custom Middleware

You can create your own middleware to add custom functionality. A common use case is to log requests, add a processing time header, or handle custom authentication schemes.

A middleware function receives two arguments:
-   `request: Request`: The incoming request object.
-   `call_next`: A function that receives the `request` and passes it to the next middleware or the actual path operation.

Example of a custom middleware that adds a `X-Process-Time` header to every response:
```python
# from src/main.py

import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```
This middleware records the time before passing the request on, waits for the response, calculates the total time, and injects a new header into the response before returning it.

### 3. Cross-Origin Resource Sharing (CORS)

**CORS** is a browser security feature that restricts a web page from making requests to a different domain, protocol, or port than the one that served the web page. This is known as the "same-origin policy."

In modern web development, it's very common to have a frontend (like a React or Vue app) running on a different domain (e.g., `localhost:3000`) than your backend API (e.g., `localhost:8000`). Without proper CORS configuration on your API, the browser will block requests from your frontend, preventing your application from working.

### 4. Configuring CORS Middleware in FastAPI

FastAPI provides a `CORSMiddleware` to handle this easily. You import it, add it to your application, and configure which origins, methods, and headers are allowed.

Example configuration from `src/main.py`:
```python
# from src/main.py

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500" # Example for Live Server in VS Code
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all standard methods
    allow_headers=["*"], # Allows all headers
)
```
This configuration allows web pages served from the specified origins to make requests to your API.

---

## Next Steps

-   Explore the `src/main.py` file to see how the `CORSMiddleware` and a custom timing middleware are implemented.
-   Run the application and use a tool like `curl -v http://localhost:8000/` or your browser's developer tools to inspect the response headers. You should see the `X-Process-Time` header.
-   Create a simple `index.html` file and use JavaScript's `fetch()` to make a request to your running API. Open the HTML file from your file system or a local server to see CORS in action.
-   Try removing one of the origins from the `allow_origins` list and see how the browser blocks the request.

---

**Tip:** Correctly configuring CORS is essential for building full-stack applications. Always be as specific as possible with `allow_origins` in a production environment to maintain security.

---