from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database.base import SharedBase

if TYPE_CHECKING:
    from src.domain.shared.users.model import Company


class Tenant(SharedBase):
    __tablename__ = "tenant"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=True)
    schema_name: Mapped[str] = mapped_column(
        String(60), nullable=False, unique=True)

    company: Mapped["Company"] = relationship(
        back_populates="tenant", lazy='joined')

    __table_args__ = ({"schema": "shared"})

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name={self.name},\
            schema_name={self.schema_name})>"
