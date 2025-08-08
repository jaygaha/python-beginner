from fastapi import FastAPI
from src.core.config import settings
from src.database.connection import create_tables
from src.routers import auth, users

# Create tables on startup
create_tables()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "FastAPI Authentication Tutorial"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
