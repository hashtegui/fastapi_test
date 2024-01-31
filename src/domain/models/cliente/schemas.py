from datetime import date

from pydantic import BaseModel, ConfigDict


class ClienteIn(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    nome: str | None = None
    email: str | None = None


class ClienteOut(ClienteIn):
    id: int
    dt_criacao: date
