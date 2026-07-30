from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(120))
    bio: Mapped[str] = mapped_column(Text)
    focus_areas: Mapped[list[str]] = mapped_column(JSON)
    avatar_seed: Mapped[str] = mapped_column(String(8))
    display_order: Mapped[int] = mapped_column()
