from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import SchemaItem

from src.domain.models import Base


class Cliente(Base):
    __tablename__ = "cliente"

    __table_args__ = (PrimaryKeyConstraint("id"), {"schema": "public"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgc: Mapped[str] = mapped_column(String(15))
    nome: Mapped[Optional[str]] = mapped_column(String(100))
    razao_social: Mapped[Optional[str]] = mapped_column(String(150))
    tipo_pessoa: Mapped[Optional[str]] = mapped_column(String(1))
    dt_criacao: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=datetime.now)
