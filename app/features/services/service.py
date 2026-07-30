from app.core.errors import NotFoundError
from app.features.services.repository import ServicesRepository
from app.features.services.schemas import ServiceOut


class ServicesService:
    def __init__(self, repository: ServicesRepository) -> None:
        self._repository = repository

    async def list(self) -> list[ServiceOut]:
        rows = await self._repository.list_ordered()
        return [ServiceOut.model_validate(row) for row in rows]

    async def get(self, slug: str) -> ServiceOut:
        service = await self._repository.get_by_slug(slug)
        if service is None:
            raise NotFoundError(f"No service with slug '{slug}'.")
        return ServiceOut.model_validate(service)
