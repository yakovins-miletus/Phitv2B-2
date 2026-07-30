from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.content_status import ContentStatus, status_column
from app.db.base import Base


class InnovationPost(Base):
    __tablename__ = "innovation_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(60))
    excerpt: Mapped[str] = mapped_column(String(400))
    body: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    author: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[ContentStatus] = mapped_column(
        status_column(), default=ContentStatus.DRAFT, index=True
    )
    published_on: Mapped[date] = mapped_column(Date)
    featured: Mapped[bool] = mapped_column(default=False)
