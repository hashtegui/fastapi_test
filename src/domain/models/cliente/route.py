from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.domain.models.cliente.schemas import ClienteIn, ClienteOut
from src.domain.models.cliente.service import ClienteService

router = APIRouter()


@router.get("/", response_model=List[ClienteOut])
async def get_all_clients(cliente_service: Annotated[ClienteService, Depends()]):

    return await cliente_service.get_clientes()


@router.post("/", response_model=ClienteOut)
async def create_client(cliente_in: ClienteIn,
                        cliente_service: Annotated[ClienteService, Depends()]):

    return await cliente_service.post_cliente(cliente_in)
