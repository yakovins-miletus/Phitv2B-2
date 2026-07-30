"""Content status enum and database column helper for Phitopolis Heimdall CMS."""

import enum
from sqlalchemy import Enum


class ContentStatus(enum.StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


def status_column() -> Enum:
    return Enum(
        ContentStatus,
        native_enum=False,
        length=12,
        values_callable=lambda e: [member.value for member in e],
    )
