from app.core.schema import ApiModel, IdStr


class SubTeamOut(ApiModel):
    name: str
    description: str


class ServiceOut(ApiModel):
    id: IdStr
    slug: str
    name: str
    tagline: str
    description: str
    icon: str
    highlights: list[str]
    display_order: int
    sub_teams: list[SubTeamOut] | None = None


class ServiceCreate(ApiModel):
    slug: str
    name: str
    tagline: str
    description: str
    icon: str
    highlights: list[str]
    display_order: int
    sub_teams: list[SubTeamOut] | None = None
