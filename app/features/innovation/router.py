from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.errors import Problem, ValidationProblem
from app.deps import PaginationDep, SessionDep
from app.features.innovation.repository import InnovationRepository
from app.features.innovation.schemas import InnovationPostOut, InnovationPostPage, InnovationSort
from app.features.innovation.service import InnovationService

router = APIRouter(prefix="/innovation-posts", tags=["innovation"])


def get_innovation_service(session: SessionDep) -> InnovationService:
    return InnovationService(InnovationRepository(session))


InnovationDep = Annotated[InnovationService, Depends(get_innovation_service)]
CategoryParam = Annotated[
    str | None, Query(min_length=1, max_length=60, pattern="^[A-Za-z0-9 &-]+$")
]
SearchParam = Annotated[str | None, Query(min_length=1, max_length=100)]
SortParam = Annotated[InnovationSort, Query()]


@router.get("", response_model=InnovationPostPage, responses={422: {"model": ValidationProblem}})
async def list_innovation_posts(
    pagination: PaginationDep,
    service: InnovationDep,
    category: CategoryParam = None,
    q: SearchParam = None,
    sort: SortParam = "newest",
) -> InnovationPostPage:
    return await service.list(
        limit=pagination.limit,
        offset=pagination.offset,
        category=category,
        q=q,
        sort=sort,
        include_drafts=False,
    )


@router.get("/{slug}", response_model=InnovationPostOut, responses={404: {"model": Problem}})
async def get_innovation_post(slug: str, service: InnovationDep) -> InnovationPostOut:
    return await service.get(slug, include_drafts=False)
