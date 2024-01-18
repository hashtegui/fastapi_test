from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database.base import SharedBase


class Tenant(SharedBase):
    __tablename__ = "tenant"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=True)
    schema_name: Mapped[str] = mapped_column(
        String(60), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name={self.name},\
            schema_name={self.schema_name})>"
