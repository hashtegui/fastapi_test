import uuid
from datetime import date

from sqlalchemy import UUID, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models import Base


class Funcionario(Base):

    __tablename__ = "funcionarios"
    __table_args__ = ({"schema": "public"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(60), nullable=True, unique=True)
    dt_criacao: Mapped[date] = mapped_column(
        Date, nullable=True, default=date.today)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
