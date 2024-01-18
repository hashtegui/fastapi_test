from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models import Base


class Pedido(Base):
    __tablename__ = 'pedidos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    quantidade: Mapped[int] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Float)
