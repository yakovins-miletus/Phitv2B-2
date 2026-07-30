from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.services.models import Service


class ServicesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_ordered(self) -> Sequence[Service]:
        result = await self._session.scalars(select(Service).order_by(Service.display_order))
        return result.all()

    async def get_by_slug(self, slug: str) -> Service | None:
        return await self._session.scalar(select(Service).where(Service.slug == slug))
