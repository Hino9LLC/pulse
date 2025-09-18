"""Company service for business logic"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Company


class CompanyService:
    """Service for company-related operations"""

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> Company | None:
        """Get company by ID"""
        stmt = select(Company).where(Company.id == company_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_company_by_uuid(self, session: AsyncSession, uuid: str) -> Company | None:
        """Get company by UUID"""
        stmt = select(Company).where(Company.uuid == uuid)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_company(self, session: AsyncSession, company_id: int) -> Company | None:
        """Get company by ID"""
        stmt = select(Company).where(Company.id == company_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_companies(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        industry: str | None = None,
    ) -> list[Company]:
        """Get list of companies with pagination and filters"""
        stmt = select(Company)

        if industry:
            stmt = stmt.where(Company.industry == industry)

        stmt = stmt.offset(skip).limit(limit).order_by(Company.company_name)
        result = await session.execute(stmt)
        return list(result.scalars().all())


# Global service instance
company_service = CompanyService()
