from typing import Annotated

from fastapi import APIRouter, Depends

from app.deps import SessionDep
from app.features.team.repository import TeamRepository
from app.features.team.schemas import TeamMemberOut
from app.features.team.service import TeamService

router = APIRouter(prefix="/team", tags=["team"])


def get_team_service(session: SessionDep) -> TeamService:
    return TeamService(TeamRepository(session))


TeamDep = Annotated[TeamService, Depends(get_team_service)]


@router.get("", response_model=list[TeamMemberOut])
async def list_team_members(service: TeamDep) -> list[TeamMemberOut]:
    return await service.list()
