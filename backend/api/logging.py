"""Structured logging middleware for request/response tracking (PHASE 3)."""
from __future__ import annotations

import json
import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests/responses in JSON format for structured analysis."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response with timing and status."""
        start_time = time.time()
        
        # Capture request info
        request_info = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
        }

        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            log_entry = {
                **request_info,
                "status": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "level": "INFO" if response.status_code < 400 else "WARN",
            }
            
            # Add query params if present
            if request.url.query:
                log_entry["query"] = str(request.url.query)
            
            print(json.dumps(log_entry))
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            log_entry = {
                **request_info,
                "status": 500,
                "error": str(e),
                "duration_ms": round(duration_ms, 2),
                "level": "ERROR",
            }
            print(json.dumps(log_entry))
            raise
