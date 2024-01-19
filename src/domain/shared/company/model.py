from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.shared import SharedBase


class Company (SharedBase):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=True)
