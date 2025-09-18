"""
Database models for Pulse
Generic SQLAlchemy models designed for SQLite with PostgreSQL migration path
"""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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

    # Text fields
    top_investors: Mapped[str] = mapped_column(Text, nullable=False)
    product: Mapped[str] = mapped_column(Text, nullable=False)
    g2_rating: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.company_name}', industry='{self.industry}')>"


class Item(Base):
    """Generic item model - keeping for reference"""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title='{self.title[:50]}...')>"


class AuditLog(Base):
    """Simple audit trail for actions and events"""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    action: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # e.g., "item.created", "user.login"
    user_id: Mapped[int | None] = mapped_column(INTEGER, nullable=True)
    resource_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # e.g., "item", "user"
    resource_id: Mapped[int | None] = mapped_column(INTEGER, nullable=True)
    data: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # JSON string for additional context
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"
