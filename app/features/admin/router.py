from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from app.deps import PaginationDep, SessionDep
from app.features.admin.schemas import AdminStats
from app.features.blog.repository import BlogRepository
from app.features.blog.schemas import BlogPostCreate, BlogPostOut, BlogPostPage, BlogPostUpdate
from app.features.blog.service import BlogService
from app.features.contact.repository import ContactRepository
from app.features.contact.schemas import ContactMessageOut
from app.features.contact.service import ContactService
from app.features.innovation.repository import InnovationRepository
from app.features.innovation.schemas import InnovationPostCreate, InnovationPostOut, InnovationPostUpdate
from app.features.innovation.service import InnovationService
from app.features.services.repository import ServicesRepository
from app.features.team.repository import TeamRepository

router = APIRouter(prefix="/heimdall/admin", tags=["admin"])


def get_blog_service(session: SessionDep) -> BlogService:
    return BlogService(BlogRepository(session))


def get_innovation_service(session: SessionDep) -> InnovationService:
    return InnovationService(InnovationRepository(session))


def get_contact_service(session: SessionDep) -> ContactService:
    return ContactService(ContactRepository(session))


BlogDep = Annotated[BlogService, Depends(get_blog_service)]
InnovationDep = Annotated[InnovationService, Depends(get_innovation_service)]
ContactDep = Annotated[ContactService, Depends(get_contact_service)]


@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    session: SessionDep,
    blog_service: BlogDep,
    contact_service: ContactDep,
) -> AdminStats:
    blog_repo = BlogRepository(session)
    services_repo = ServicesRepository(session)
    team_repo = TeamRepository(session)

    all_blogs, total_blogs = await blog_repo.list_page(limit=1000, offset=0, category=None, include_drafts=True)
    published = sum(1 for b in all_blogs if b.status == "published")
    drafts = total_blogs - published

    contact_count = await contact_service.count_messages()
    services_list = await services_repo.list_ordered()
    team_list = await team_repo.list_ordered()

    return AdminStats(
        total_blog_posts=total_blogs,
        published_blog_posts=published,
        draft_blog_posts=drafts,
        total_contact_messages=contact_count,
        total_services=len(services_list),
        total_team_members=len(team_list),
    )


@router.get("/blogs", response_model=BlogPostPage)
async def list_all_blogs_admin(
    pagination: PaginationDep,
    service: BlogDep,
    category: str | None = None,
    q: str | None = None,
) -> BlogPostPage:
    return await service.list(
        limit=pagination.limit,
        offset=pagination.offset,
        category=category,
        q=q,
        include_drafts=True,
    )


@router.post("/blogs", response_model=BlogPostOut, status_code=status.HTTP_201_CREATED)
async def create_blog_admin(payload: BlogPostCreate, service: BlogDep) -> BlogPostOut:
    return await service.create(payload)


@router.put("/blogs/{slug}", response_model=BlogPostOut)
async def update_blog_admin(slug: str, payload: BlogPostUpdate, service: BlogDep) -> BlogPostOut:
    return await service.update(slug, payload)


@router.delete("/blogs/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_admin(slug: str, service: BlogDep) -> None:
    await service.delete(slug)


@router.get("/contact-messages", response_model=list[ContactMessageOut])
async def list_contact_messages_admin(
    service: ContactDep,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ContactMessageOut]:
    messages, _ = await service.list_messages(limit=limit, offset=offset)
    return messages
