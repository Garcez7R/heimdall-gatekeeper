"""PHASE 1: Security middleware for rate limiting and authentication."""
from __future__ import annotations

import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["600 per minute"],  # 10 req/sec default
    storage_uri=None,  # In-memory for demo; use Redis for production
)

JWT_SECRET = os.getenv(
    "HEIMDALL_JWT_SECRET",
    os.getenv("JWT_SECRET", "heimdall-demo-key-change-in-production"),
)
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


def create_jwt_token(data: dict, expires_hours: int = JWT_EXPIRY_HOURS) -> str:
    """Generate JWT token for API authentication."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_api_key(request: Request) -> str:
    """PHASE 1: Verify X-Heimdall-Key header for ingest endpoints."""
    api_key = request.headers.get("X-Heimdall-Key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing X-Heimdall-Key header",
        )
    if api_key != os.getenv("HEIMDALL_API_KEY", "demo-key"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key
