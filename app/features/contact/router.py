from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.errors import ValidationProblem
from app.deps import SessionDep
from app.features.contact.repository import ContactRepository
from app.features.contact.schemas import ContactMessageIn, ContactMessageOut
from app.features.contact.service import ContactService

router = APIRouter(prefix="/contact-messages", tags=["contact"])


def get_contact_service(session: SessionDep) -> ContactService:
    return ContactService(ContactRepository(session))


ContactDep = Annotated[ContactService, Depends(get_contact_service)]


@router.post(
    "",
    response_model=ContactMessageOut,
    status_code=201,
    responses={422: {"model": ValidationProblem}},
)
async def create_contact_message(
    payload: ContactMessageIn, service: ContactDep
) -> ContactMessageOut:
    return await service.submit(payload)
