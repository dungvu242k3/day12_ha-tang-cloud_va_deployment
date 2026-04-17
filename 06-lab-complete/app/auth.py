"""
Authentication Module — API Key + JWT

Hỗ trợ 2 phương thức xác thực:
  1. API Key: Đơn giản, phù hợp cho server-to-server
  2. JWT: Phù hợp cho end-user authentication
"""
import os
import time
import logging
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(
    api_key: str = Security(api_key_header),
) -> str:
    """
    Xác thực API Key từ header X-API-Key.
    Raise 401 nếu key không hợp lệ.
    """
    from app.config import settings

    if not api_key or api_key != settings.agent_api_key:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include header: X-API-Key: <key>",
        )
    return api_key


def create_jwt_token(username: str, role: str) -> str:
    """Tạo JWT token với expiry 60 phút."""
    try:
        import jwt
    except ImportError:
        raise HTTPException(500, "PyJWT not installed")

    from app.config import settings

    now = int(time.time())
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_jwt_token(token: str) -> dict:
    """Xác thực JWT token, trả về payload."""
    try:
        import jwt
    except ImportError:
        raise HTTPException(500, "PyJWT not installed")

    from app.config import settings

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
