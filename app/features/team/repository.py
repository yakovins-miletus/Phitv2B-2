from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.team.models import TeamMember


class TeamRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_ordered(self) -> Sequence[TeamMember]:
        result = await self._session.scalars(select(TeamMember).order_by(TeamMember.display_order))
        return result.all()
