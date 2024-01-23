from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str


class UserIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    password: str = Field(min_length=4)
    company_id: int
