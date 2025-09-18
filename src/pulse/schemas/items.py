"""Item schemas for API requests and responses"""

from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item schema"""

    title: str
    content: str


class ItemCreate(ItemBase):
    """Schema for creating a new item"""


class ItemUpdate(BaseModel):
    """Schema for updating an item"""

    title: str | None = None
    content: str | None = None


class ItemResponse(ItemBase):
    """Schema for item responses"""

    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Alias for backward compatibility
ItemWithUser = ItemResponse
