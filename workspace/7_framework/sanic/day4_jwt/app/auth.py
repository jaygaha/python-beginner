"""
Basic JWT helper and middleware.
"""
import jwt
from sanic.exceptions import Unauthorized
from sanic.request import Request

# In real application, this should be stored securely
JWT_SECRET = "your_secret_key_123"
JWT_ALGORITHM = "HS256"

def create_token(user_id: int) -> str:
    payload = {"user_id": user_id}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
    except jwt.PyJWTError:
        raise Unauthorized("Invalid or expired token")

async def auth_middleware(request: Request):
    if request.path.startswith("/api/secure"):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Unauthorized("Missing Bearer token")

        token = auth_header.split()[1]
        payload = decode_token(token)
        request.ctx.user = payload.get("user_id")
