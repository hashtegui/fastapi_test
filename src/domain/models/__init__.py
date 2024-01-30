from src.config.database.base import Base

from .cliente.model import Cliente
from .funcionario.model import Funcionario
from .pedido.model import Pedido
from .precos.model import Preco

__all__ = [
    "Base",
    "Cliente",
    "Pedido",
    "Preco",
    "Funcionario"

]
