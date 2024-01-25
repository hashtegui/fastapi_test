from pydantic import BaseModel, ConfigDict, Field


class CompanyIn(BaseModel):
    name: str
    tenant_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class CompanyOut(BaseModel):
    id: int
    name: str
    tenant_id: int


class CompanyFilter:
    def __init__(self,
                 name: str | None = None,
                 id: int | None = None,
                 tenant_id: int | None = None) -> None:

        self.name = name
        self.id = id
        self.tenant_id = tenant_id

    def __repr__(self) -> str:
        return f'<CompanyFilter(id={self.id}, name={self.name}, tenant_id={self.tenant_id})>'
