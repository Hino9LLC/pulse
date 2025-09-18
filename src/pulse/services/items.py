"""Item service for business logic"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Item


class ItemService:
    """Service for item-related operations"""

    async def get_item_by_id(self, session: AsyncSession, item_id: int) -> Item | None:
        """Get item by ID"""
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_item_by_uuid(self, session: AsyncSession, uuid: str) -> Item | None:
        """Get item by UUID"""
        stmt = select(Item).where(Item.uuid == uuid)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_item(self, session: AsyncSession, item_id: int) -> Item | None:
        """Get item by ID"""
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_items(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        """Get list of items with pagination and filters"""
        stmt = select(Item)

        stmt = stmt.offset(skip).limit(limit).order_by(Item.created_at.desc())
        result = await session.execute(stmt)
        return list(result.scalars().all())


# Global service instance
item_service = ItemService()
