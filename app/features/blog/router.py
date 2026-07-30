from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.errors import Problem, ValidationProblem
from app.deps import PaginationDep, SessionDep
from app.features.blog.repository import BlogRepository
from app.features.blog.schemas import BlogPostOut, BlogPostPage, BlogSort
from app.features.blog.service import BlogService

router = APIRouter(prefix="/blog-posts", tags=["blog"])


def get_blog_service(session: SessionDep) -> BlogService:
    return BlogService(BlogRepository(session))


BlogDep = Annotated[BlogService, Depends(get_blog_service)]
CategoryParam = Annotated[
    str | None, Query(min_length=1, max_length=60, pattern="^[A-Za-z0-9 &-]+$")
]
SearchParam = Annotated[str | None, Query(min_length=1, max_length=100)]
SortParam = Annotated[BlogSort, Query()]


@router.get("", response_model=BlogPostPage, responses={422: {"model": ValidationProblem}})
async def list_blog_posts(
    pagination: PaginationDep,
    service: BlogDep,
    category: CategoryParam = None,
    q: SearchParam = None,
    sort: SortParam = "newest",
) -> BlogPostPage:
    return await service.list(
        limit=pagination.limit,
        offset=pagination.offset,
        category=category,
        q=q,
        sort=sort,
        include_drafts=False,
    )


@router.get("/{slug}", response_model=BlogPostOut, responses={404: {"model": Problem}})
async def get_blog_post(slug: str, service: BlogDep) -> BlogPostOut:
    return await service.get(slug, include_drafts=False)
