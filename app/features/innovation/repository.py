from collections.abc import Sequence
from sqlalchemy import UnaryExpression, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.content_status import ContentStatus
from app.features.innovation.models import InnovationPost
from app.features.innovation.schemas import InnovationPostCreate, InnovationPostUpdate, InnovationSort

_ORDERINGS: dict[InnovationSort, tuple[UnaryExpression[object], ...]] = {
    "newest": (InnovationPost.published_on.desc(), InnovationPost.id.desc()),
    "oldest": (InnovationPost.published_on.asc(), InnovationPost.id.asc()),
    "title_az": (func.lower(InnovationPost.title).asc(), InnovationPost.id.desc()),
    "title_za": (func.lower(InnovationPost.title).desc(), InnovationPost.id.desc()),
}


class InnovationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        category: str | None,
        q: str | None = None,
        sort: InnovationSort = "newest",
        include_drafts: bool = False,
    ) -> tuple[Sequence[InnovationPost], int]:
        query = select(InnovationPost)
        if not include_drafts:
            query = query.where(InnovationPost.status == ContentStatus.PUBLISHED)
        if category is not None:
            query = query.where(InnovationPost.category == category)
        if q is not None:
            query = query.where(
                InnovationPost.title.icontains(q, autoescape=True)
                | InnovationPost.excerpt.icontains(q, autoescape=True)
                | InnovationPost.author.icontains(q, autoescape=True)
            )
        total = await self._session.scalar(select(func.count()).select_from(query.subquery()))
        rows = await self._session.scalars(
            query.order_by(*_ORDERINGS[sort]).limit(limit).offset(offset)
        )
        return rows.all(), total or 0

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> InnovationPost | None:
        query = select(InnovationPost).where(InnovationPost.slug == slug)
        if not include_drafts:
            query = query.where(InnovationPost.status == ContentStatus.PUBLISHED)
        return await self._session.scalar(query)

    async def create(self, payload: InnovationPostCreate) -> InnovationPost:
        post = InnovationPost(**payload.model_dump())
        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def update(self, post: InnovationPost, payload: InnovationPostUpdate) -> InnovationPost:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def delete(self, post: InnovationPost) -> None:
        await self._session.delete(post)
        await self._session.commit()
