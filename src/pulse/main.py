"""
FastAPI application for Pulse
Main application entry point with lifespan management
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.session import close_database, init_database
from .logging import configure_logging
from .middleware.request_id import RequestIdMiddleware
from .middleware.timing import TimingMiddleware
from .routes import companies, health, items
from .settings import settings


logger = logging.getLogger("pulse")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan management"""
    # Startup
    configure_logging()
    logger.info("Starting Pulse", extra={"env": settings.env})

    # Initialize database
    await init_database()
    logger.info("Database initialized")

    yield

    # Shutdown
    await close_database()
    logger.info("Pulse stopped")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Pulse - Modern FastAPI + React scaffolding for rapid experimentation",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(RequestIdMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(items.router, prefix="/api/items", tags=["items"])


@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "message": "Welcome to Pulse! Check /docs for API documentation.",
        "docs_url": "/docs",
        "health_check": "/api/health",
    }
