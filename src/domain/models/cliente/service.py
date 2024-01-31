from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from src.auth.context import Context
from src.domain.models.cliente.model import Cliente
from src.domain.models.cliente.schemas import ClienteIn


class ClienteService:
    def __init__(self,
                 context: Annotated[Context, Depends()]) -> None:

        self.session = context.session
        self.usuario_logado = context.user

    async def get_clientes(self):
        result = await self.session.scalars(select(Cliente))
        return result.all()

    async def post_cliente(self, cliente_in: ClienteIn):
        cliente = Cliente(**cliente_in.model_dump())
        self.session.add(cliente)
        await self.session.commit()
        await self.session.refresh(cliente)
        return cliente
