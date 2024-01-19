from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models import Base


class Preco(Base):
    __tablename__ = 'precos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    preco: Mapped[float] = mapped_column(Float)
