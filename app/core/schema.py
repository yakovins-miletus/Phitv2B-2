from typing import Annotated
from pydantic import BaseModel, BeforeValidator, ConfigDict

IdStr = Annotated[str, BeforeValidator(str)]


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Page[T](BaseModel):
    items: list[T]
    total: int
    limit: int
    offset: int
