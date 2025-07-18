"""
JWT + middleware
"""
import os
import jwt
import bcrypt
from sanic.exceptions import Unauthorized

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"

def create_token(user_id):
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise Unauthorized("Invalid token")

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

async def auth_middleware(request):
    if request.path.startswith("/api/secure"):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            raise Unauthorized("Missing Bearer token")
        payload = decode_token(token)
        request.ctx.user_id = payload.get("user_id")
