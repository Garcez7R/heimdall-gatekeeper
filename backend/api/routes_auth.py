"""Authentication endpoints for JWT token generation (PHASE 3)."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(tags=["auth"], prefix="/api/auth")

# Demo credentials (PHASE 3: integrate with LDAP, OAuth2, etc.)
DEMO_USERS = {
    "admin": "admin123",  # Password in demo only
    "analyst": "analyst123",
}

# JWT secret from environment or demo default
JWT_SECRET = os.environ.get("HEIMDALL_JWT_SECRET", "demo-secret-key-phase3-2026")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


class LoginRequest(BaseModel):
    """Login request with username and password."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str
    expires_in: int  # seconds


@router.post("/login")
def login(request: LoginRequest) -> LoginResponse:
    """Generate JWT token for authenticated user.
    
    Demo mode accepts test credentials:
    - username: admin, password: admin123
    - username: analyst, password: analyst123
    
    PHASE 3: Replace with LDAP integration or OAuth2 provider.
    """
    # Validate credentials (demo mode)
    if request.username not in DEMO_USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if DEMO_USERS[request.username] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Generate JWT token
    from backend.api.middleware import create_jwt_token

    role = "admin" if request.username == "admin" else "analyst"
    token_payload = {
        "username": request.username,
        "role": role,
        "exp": (datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS)).timestamp(),
    }

    token = create_jwt_token(token_payload)
    expires_in = int(JWT_EXPIRY_HOURS * 3600)

    return LoginResponse(
        access_token=token,
        token_type="Bearer",
        expires_in=expires_in,
    )
