"""Company schemas for API requests and responses"""

from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    """Base company schema"""

    company_name: str
    founded_year: int
    headquarters: str
    industry: str
    total_funding_usd: int
    arr_usd: int
    valuation_usd: int
    employee_count: int | None
    top_investors: str
    product: str
    g2_rating: float


class CompanyResponse(CompanyBase):
    """Schema for company responses"""

    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
