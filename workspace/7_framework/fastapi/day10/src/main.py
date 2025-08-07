import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from .dependencies import limiter

# --- Lifespan Events for Caching ---
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

# Create the FastAPI app instance
app = FastAPI(lifespan=lifespan)

# Attach the limiter instance to the application's state
# This is the crucial step to make the limiter accessible to the middleware.
app.state.limiter = limiter

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




# --- Background Task Function ---
def write_log(message: str):
    """
    A simple background task that writes a message to a log file.
    """
    with open("log.txt", mode="a") as log_file:
        log_file.write(message)
    print(f"Log written: {message.strip()}")


# --- API Endpoints ---

@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"status": "API is running"}

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

@app.get("/rate-limited")
@limiter.limit("5/minute")  # Allow 5 requests per minute
async def get_rate_limited_endpoint(request: Request):
    """
    This endpoint is rate-limited.
    It allows a maximum of 5 requests per minute from the same IP address.
    """
    return {"detail": "This endpoint is rate-limited."}

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
