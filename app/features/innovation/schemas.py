from datetime import date
from typing import Literal

from app.core.content_status import ContentStatus
from app.core.schema import ApiModel, IdStr, Page

InnovationSort = Literal["newest", "oldest", "title_az", "title_za"]


class InnovationPostSummary(ApiModel):
    id: IdStr
    slug: str
    title: str
    category: str
    excerpt: str
    image_url: str | None
    author: str | None
    published_on: date
    featured: bool


class InnovationPostOut(InnovationPostSummary):
    body: str


class InnovationPostPage(Page[InnovationPostSummary]):
    pass


class InnovationPostCreate(ApiModel):
    slug: str
    title: str
    category: str
    excerpt: str
    body: str
    image_url: str | None = None
    author: str | None = None
    status: ContentStatus = ContentStatus.DRAFT
    published_on: date
    featured: bool = False


class InnovationPostUpdate(ApiModel):
    slug: str | None = None
    title: str | None = None
    category: str | None = None
    excerpt: str | None = None
    body: str | None = None
    image_url: str | None = None
    author: str | None = None
    status: ContentStatus | None = None
    published_on: date | None = None
    featured: bool | None = None
