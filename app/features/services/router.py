from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.errors import Problem
from app.deps import SessionDep
from app.features.services.repository import ServicesRepository
from app.features.services.schemas import ServiceOut
from app.features.services.service import ServicesService

router = APIRouter(prefix="/services", tags=["services"])


def get_services_service(session: SessionDep) -> ServicesService:
    return ServicesService(ServicesRepository(session))


ServiceDep = Annotated[ServicesService, Depends(get_services_service)]


@router.get("", response_model=list[ServiceOut])
async def list_services(service: ServiceDep) -> list[ServiceOut]:
    return await service.list()


@router.get("/{slug}", response_model=ServiceOut, responses={404: {"model": Problem}})
async def get_service(slug: str, service: ServiceDep) -> ServiceOut:
    return await service.get(slug)
