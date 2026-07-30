from app.core.schema import ApiModel, IdStr


class TeamMemberOut(ApiModel):
    id: IdStr
    name: str
    role: str
    bio: str
    focus_areas: list[str]
    avatar_seed: str
    display_order: int


class TeamMemberCreate(ApiModel):
    name: str
    role: str
    bio: str
    focus_areas: list[str]
    avatar_seed: str
    display_order: int
