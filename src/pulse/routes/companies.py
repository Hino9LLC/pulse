"""Company routes for SaaS companies data"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_session
from ..schemas.companies import CompanyResponse
from ..services.companies import company_service


router = APIRouter()


@router.get("/", response_model=list[CompanyResponse])
async def get_companies(
    skip: int = Query(0, ge=0, description="Number of companies to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of companies to return"),
    industry: str = Query(None, description="Filter by industry"),
    session: AsyncSession = Depends(get_session),
):
    """Get list of companies with pagination and filters"""
    companies = await company_service.get_companies(
        session, skip=skip, limit=limit, industry=industry
    )
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific company by ID"""
    company = await company_service.get_company(session, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company
