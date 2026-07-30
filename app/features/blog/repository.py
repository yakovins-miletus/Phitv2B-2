from collections.abc import Sequence
from sqlalchemy import UnaryExpression, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.content_status import ContentStatus
from app.features.blog.models import BlogPost
from app.features.blog.schemas import BlogPostCreate, BlogPostUpdate, BlogSort

_ORDERINGS: dict[BlogSort, tuple[UnaryExpression[object], ...]] = {
    "newest": (BlogPost.published_on.desc(), BlogPost.id.desc()),
    "oldest": (BlogPost.published_on.asc(), BlogPost.id.asc()),
    "title_az": (func.lower(BlogPost.title).asc(), BlogPost.id.desc()),
    "title_za": (func.lower(BlogPost.title).desc(), BlogPost.id.desc()),
}


class BlogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        category: str | None,
        q: str | None = None,
        sort: BlogSort = "newest",
        include_drafts: bool = False,
    ) -> tuple[Sequence[BlogPost], int]:
        query = select(BlogPost)
        if not include_drafts:
            query = query.where(BlogPost.status == ContentStatus.PUBLISHED)
        if category is not None:
            query = query.where(BlogPost.category == category)
        if q is not None:
            query = query.where(
                BlogPost.title.icontains(q, autoescape=True)
                | BlogPost.excerpt.icontains(q, autoescape=True)
                | BlogPost.author.icontains(q, autoescape=True)
            )
        total = await self._session.scalar(select(func.count()).select_from(query.subquery()))
        rows = await self._session.scalars(
            query.order_by(*_ORDERINGS[sort]).limit(limit).offset(offset)
        )
        return rows.all(), total or 0

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> BlogPost | None:
        query = select(BlogPost).where(BlogPost.slug == slug)
        if not include_drafts:
            query = query.where(BlogPost.status == ContentStatus.PUBLISHED)
        return await self._session.scalar(query)

    async def create(self, payload: BlogPostCreate) -> BlogPost:
        post = BlogPost(**payload.model_dump())
        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def update(self, post: BlogPost, payload: BlogPostUpdate) -> BlogPost:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def delete(self, post: BlogPost) -> None:
        await self._session.delete(post)
        await self._session.commit()
