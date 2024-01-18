from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(60), nullable=True)
    email = Column(String(60), nullable=True)
