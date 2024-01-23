from pydantic import BaseModel, ConfigDict, Field


class CompanyIn(BaseModel):
    name: str
    tenant_id: int | None = None
    model_config = ConfigDict(from_attributes=True)
