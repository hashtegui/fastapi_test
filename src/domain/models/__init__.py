from src.config.database.base import Base

from .cliente.model import Cliente
from .pedido.model import Pedido

__all__ = [
    "Base",
    "Cliente",
    "Pedido"

]
