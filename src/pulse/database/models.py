"""
Database models for Pulse
Generic SQLAlchemy models designed for SQLite with PostgreSQL migration path
"""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all database models"""


class Company(Base):
    """Company model for SaaS companies data"""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    # Company details from CSV
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    founded_year: Mapped[int] = mapped_column(Integer, nullable=False)
    headquarters: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(255), nullable=False)

    # Financial data (normalized to USD values as whole dollars, 0 if unknown)
    total_funding_usd: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)  # In USD
    arr_usd: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0
    )  # Annual Recurring Revenue in USD
    valuation_usd: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0
    )  # Valuation in USD

    # Employee count (normalized to integer)
    employee_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # JSON fields - arrays of strings
    top_investors: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    product: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    g2_rating: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.company_name}', industry='{self.industry}')>"
