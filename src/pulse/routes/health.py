"""Health check endpoints"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_session


router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "service": "pulse"}


@router.get("/healthz")
async def kubernetes_health():
    """Kubernetes-style health check"""
    return {"status": "ok"}


@router.get("/readyz")
async def readiness_check(session: AsyncSession = Depends(get_session)):
    """Readiness check with database connectivity"""
    try:
        # Simple database connectivity test
        from sqlalchemy import text

        await session.execute(text("SELECT 1"))
        return {"status": "ready", "timestamp": datetime.now().isoformat(), "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "not ready", "database": "disconnected", "error": str(e)},
        ) from e
