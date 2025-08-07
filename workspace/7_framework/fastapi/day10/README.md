# FastAPI Day 10: Advanced Features - Caching, Rate Limiting, and Background Tasks

Welcome to **Day 10** of the FastAPI tutorial series! Today, we're moving beyond the basics to explore advanced features that are essential for building robust, scalable, and production-ready applications. You'll learn how to implement caching to improve performance, rate limiting to protect your API from abuse, and background tasks to handle long-running operations without blocking the client.

---

## What You'll Learn

-   **Response Caching**: Implement caching with `fastapi-cache2` and a Redis backend to dramatically reduce response times for frequent requests.
-   **Rate Limiting**: Use `slowapi` to apply flexible rate limits to your endpoints, preventing individual users from overwhelming the service.
-   **Background Tasks**: Leverage FastAPI's built-in `BackgroundTasks` to execute operations (like writing to a log or sending an email) after a response has been sent to the client.
-   **Application Lifespan Events**: Use the `lifespan` context manager to run setup and teardown logic (like initializing a cache connection) when the application starts and stops.
-   **Custom Middleware & Exception Handling**: Integrate third-party middleware and write custom exception handlers to manage application-wide concerns like rate limiting.
-   **Testing Advanced Features**: Write unit tests to verify that caching, rate limiting, and background tasks are all functioning as expected.

---

## Key Concepts

For this tutorial, we've simplified the structure to focus on the new concepts within a single `src` directory.

-   `src/main.py`: The application's entry point. It initializes the FastAPI app and contains all the logic for caching, rate limiting, and background tasks.
-   `src/dependencies.py`: Defines the `slowapi` limiter instance.
-   `tests/test_main.py`: Contains unit tests for all the API endpoints and their advanced features.
-   `requirements.txt`: Lists the new dependencies: `redis`, `slowapi`, and `fastapi-cache2`.

### 1. Caching with `fastapi-cache2` and Redis

Caching is a powerful technique for improving API performance. Instead of re-computing a result for every request, we can store it temporarily and serve the stored version for subsequent requests.

-   **Lifespan Event**: We use the `lifespan` async context manager to initialize the Redis cache when the application starts and properly close the connection when it shuts down. This is the modern replacement for startup/shutdown events.

    ```python-beginner/workspace/7_framework/fastapi/day10/src/main.py#L13-L27
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        This function is executed when the application starts.
        It initializes the Redis connection and the FastAPI Caching.
        """
        # Connect to your Redis instance
        redis = aioredis.from_url("redis://localhost")
        # Initialize the cache with the Redis backend
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        print("FastAPI application startup complete. Cache initialized.")

        try:
            yield
        finally:
            await redis.close()
    ```

-   **The `@cache` Decorator**: Applying the `@cache` decorator to an endpoint is all it takes to enable caching. The `expire` argument specifies how long the response should be cached, in seconds.

    ```python-beginner/workspace/7_framework/fastapi/day10/src/main.py#L93-L102
    @app.get("/cached-data")
    @cache(expire=30)  # Cache this response for 30 seconds
    async def get_cached_data():
        """
        This endpoint demonstrates caching.
        The first time it's called, it will "process" for 2 seconds.
        Subsequent calls within 30 seconds will return the cached response instantly.
        """
        print("Processing request to get cached data...")
        time.sleep(2)  # Simulate a slow operation
        return {"detail": "This is some cached data", "timestamp": time.time()}
    ```

### 2. Rate Limiting with `slowapi`

Rate limiting is crucial for preventing abuse and ensuring your API remains available for all users. We use the `slowapi` library, which integrates smoothly with FastAPI.

-   **Limiter Instance**: We create a `Limiter` instance that uses the client's IP address to identify unique users.

    ```python-beginner/workspace/7_framework/fastapi/day10/src/dependencies.py#L4-L5
    # Create a Limiter instance that uses the client's IP address as the key.
    limiter = Limiter(key_func=get_remote_address)
    ```

-   **Middleware and Exception Handler**: The `SlowAPIMiddleware` is added to the application to process requests. We also add a custom exception handler to return a clear JSON response when a user exceeds the rate limit.

    ```python-beginner/workspace/7_framework/fastapi/day10/src/main.py#L36-L51
    # Add the SlowAPI middleware to handle rate limiting
    app.add_middleware(SlowAPIMiddleware)

    # Define a custom exception handler for RateLimitExceeded
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        """
        Custom exception handler for rate-limited requests.
        Returns a JSON response with a 429 status code.
        """
        return JSONResponse(
            status_code=429,
            content={"detail": f"Rate limit exceeded: {exc.detail}"}
        )
    ```

-   **The `@limiter.limit` Decorator**: To protect an endpoint, we apply the `@limiter.limit` decorator with a specific limit (e.g., "5/minute").

    ```python-beginner/workspace/7_framework/fastapi/day10/src/main.py#L104-L111
    @app.get("/rate-limited")
    @limiter.limit("5/minute")  # Allow 5 requests per minute
    async def get_rate_limited_endpoint(request: Request):
        """
        This endpoint is rate-limited.
        It allows a maximum of 5 requests per minute from the same IP address.
        """
        return {"detail": "This endpoint is rate-limited."}
    ```

### 3. Background Tasks

For operations that don't need to complete before sending a response, FastAPI provides a `BackgroundTasks` dependency. This is perfect for tasks like sending confirmation emails, processing data, or writing logs.

-   **Injecting `BackgroundTasks`**: Simply add `background_tasks: BackgroundTasks` to your path operation function's signature.
-   **Adding a Task**: Use the `background_tasks.add_task()` method, passing the function to run and its arguments. The API will immediately return a response to the client while the task executes in the background.

    ```python-beginner/workspace/7_framework/fastapi/day10/src/main.py#L113-L122
    @app.post("/background-task")
    async def trigger_background_task(background_tasks: BackgroundTasks):
        """
        This endpoint triggers a background task.
        It immediately returns a response to the client while the task
        (writing to a log file) runs in the background.
        """
        # Add the task to be executed in the background
        background_tasks.add_task(write_log, "Task started: Processing data in the background.\n")
        return {"message": "Background task has been initiated."}
    ```

### 4. Testing These Features

Our `tests/test_main.py` file demonstrates how to effectively test these advanced features:
-   **Testing Caching**: We call the cached endpoint twice. The first call's duration is asserted to be slow, while the second is fast. We also assert that the `timestamp` in the response body is identical for both calls, proving the data came from the cache.
-   **Testing Rate Limiting**: We loop to hit the rate-limited endpoint just enough times to succeed, then make one more call and assert that we receive a `429 Too Many Requests` status code.
-   **Testing Background Tasks**: We call the endpoint and then check for the side effect of the task—in this case, we assert that a log file has been created and contains the expected content.

---

## Next Steps

-   Make sure you have Redis running on your local machine.
-   Install the new dependencies: `pip install -r requirements.txt`.
-   Run the application with `uvicorn src.main:app --reload`.
-   Use an API client like `curl` or Postman to test the endpoints.
    -   Hit `GET /cached-data` twice and observe the difference in response time.
    -   Hit `GET /rate-limited` six times in under a minute to see the rate limit kick in.
    -   Call `POST /background-task` and check for the `log.txt` file in your project root.
-   Run the automated tests with `python -m pytest`.

---