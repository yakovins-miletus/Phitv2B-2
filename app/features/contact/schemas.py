import html
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.schema import ApiModel, IdStr


class ContactMessageIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(max_length=254)
    subject: str = Field(min_length=3, max_length=150)
    message: str = Field(min_length=10, max_length=4000)
    company_website: str = Field(
        default="",
        max_length=200,
        description="Honeypot field 1 — leave empty.",
    )
    website_hp: str = Field(
        default="",
        max_length=200,
        description="Honeypot field 2 — leave empty.",
    )

    @field_validator("name", "subject", "message")
    @classmethod
    def sanitize_html_tags(cls, v: str) -> str:
        return html.escape(v.strip())


class ContactMessageOut(ApiModel):
    id: IdStr
    name: str
    email: EmailStr
    subject: str
    message: str
    created_at: datetime
