from collections.abc import Sequence
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.contact.models import ContactMessage


class ContactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, *, name: str, email: str, subject: str, message: str) -> ContactMessage:
        row = ContactMessage(name=name, email=email, subject=subject, message=message)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return row

    async def list_all(self, *, limit: int = 50, offset: int = 0) -> tuple[Sequence[ContactMessage], int]:
        total = await self._session.scalar(select(func.count()).select_from(ContactMessage))
        rows = await self._session.scalars(
            select(ContactMessage).order_by(ContactMessage.created_at.desc()).limit(limit).offset(offset)
        )
        return rows.all(), total or 0

    async def count_all(self) -> int:
        count = await self._session.scalar(select(func.count()).select_from(ContactMessage))
        return count or 0
