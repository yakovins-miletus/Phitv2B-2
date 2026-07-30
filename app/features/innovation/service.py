from app.core.errors import NotFoundError
from app.features.blog.body_images import first_image_paragraph
from app.features.innovation.repository import InnovationRepository
from app.features.innovation.schemas import (
    InnovationPostCreate,
    InnovationPostOut,
    InnovationPostPage,
    InnovationPostSummary,
    InnovationPostUpdate,
    InnovationSort,
)


class InnovationService:
    def __init__(self, repository: InnovationRepository) -> None:
        self._repository = repository

    async def list(
        self,
        *,
        limit: int,
        offset: int,
        category: str | None,
        q: str | None = None,
        sort: InnovationSort = "newest",
        include_drafts: bool = False,
    ) -> InnovationPostPage:
        rows, total = await self._repository.list_page(
            limit=limit,
            offset=offset,
            category=category,
            q=q,
            sort=sort,
            include_drafts=include_drafts,
        )
        items = []
        for row in rows:
            summary = InnovationPostSummary.model_validate(row)
            if summary.image_url is None:
                summary.image_url = first_image_paragraph(row.body)
            items.append(summary)
        return InnovationPostPage(items=items, total=total, limit=limit, offset=offset)

    async def get(self, slug: str, *, include_drafts: bool = False) -> InnovationPostOut:
        post = await self._repository.get_by_slug(slug, include_drafts=include_drafts)
        if post is None:
            raise NotFoundError(f"No innovation post with slug '{slug}'.")
        return InnovationPostOut.model_validate(post)

    async def create(self, payload: InnovationPostCreate) -> InnovationPostOut:
        existing = await self._repository.get_by_slug(payload.slug, include_drafts=True)
        if existing:
            raise ValueError(f"Innovation post with slug '{payload.slug}' already exists.")
        post = await self._repository.create(payload)
        return InnovationPostOut.model_validate(post)

    async def update(self, slug: str, payload: InnovationPostUpdate) -> InnovationPostOut:
        post = await self._repository.get_by_slug(slug, include_drafts=True)
        if post is None:
            raise NotFoundError(f"No innovation post with slug '{slug}'.")
        updated = await self._repository.update(post, payload)
        return InnovationPostOut.model_validate(updated)

    async def delete(self, slug: str) -> None:
        post = await self._repository.get_by_slug(slug, include_drafts=True)
        if post is None:
            raise NotFoundError(f"No innovation post with slug '{slug}'.")
        await self._repository.delete(post)
