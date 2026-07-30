import logging
from datetime import UTC, datetime
from uuid import uuid4

from app.features.contact.repository import ContactRepository
from app.features.contact.schemas import ContactMessageIn, ContactMessageOut

logger = logging.getLogger("heimdall")


class ContactService:
    def __init__(self, repository: ContactRepository) -> None:
        self._repository = repository

    async def submit(self, data: ContactMessageIn) -> ContactMessageOut:
        if data.company_website or data.website_hp:
            logger.info("Honeypot tripped on contact form; message discarded.")
            return ContactMessageOut(
                id=uuid4().hex,
                name=data.name,
                email=data.email,
                subject=data.subject,
                message=data.message,
                created_at=datetime.now(tz=UTC),
            )
        row = await self._repository.add(
            name=data.name, email=data.email, subject=data.subject, message=data.message
        )
        return ContactMessageOut.model_validate(row)

    async def list_messages(self, limit: int = 50, offset: int = 0) -> tuple[list[ContactMessageOut], int]:
        rows, total = await self._repository.list_all(limit=limit, offset=offset)
        return [ContactMessageOut.model_validate(row) for row in rows], total

    async def count_messages(self) -> int:
        return await self._repository.count_all()
