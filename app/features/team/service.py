from app.features.team.repository import TeamRepository
from app.features.team.schemas import TeamMemberOut


class TeamService:
    def __init__(self, repository: TeamRepository) -> None:
        self._repository = repository

    async def list(self) -> list[TeamMemberOut]:
        rows = await self._repository.list_ordered()
        return [TeamMemberOut.model_validate(row) for row in rows]
