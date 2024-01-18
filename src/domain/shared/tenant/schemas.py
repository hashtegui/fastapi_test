from pydantic import BaseModel, ConfigDict


class TenantIn(BaseModel):
    name: str
    schema_name: str

    model_config = ConfigDict(from_attributes=True)


class TenantOut(TenantIn):
    id: int
