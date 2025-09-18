"""Item management routes"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_session
from ..schemas.items import ItemWithUser
from ..services.items import item_service


router = APIRouter()


@router.get("/", response_model=list[ItemWithUser])
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    session: AsyncSession = Depends(get_session),
):
    """Get list of items with pagination and filters"""
    items = await item_service.get_items(session, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=ItemWithUser)
async def get_item(
    item_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific item by ID"""
    item = await item_service.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
