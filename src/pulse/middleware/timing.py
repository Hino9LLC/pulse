"""Request timing middleware"""

import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..logging import get_logger


logger = get_logger("pulse.timing")


class TimingMiddleware(BaseHTTPMiddleware):
    """Log request timing information"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        # Get request ID if available
        request_id = getattr(request.state, "request_id", None)

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.perf_counter() - start_time

        # Log request details
        logger.info(
            "Request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )

        # Add timing header
        response.headers["X-Process-Time"] = f"{duration:.4f}"

        return response
