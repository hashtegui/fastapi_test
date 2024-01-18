import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.shared import SharedBase


class User(SharedBase):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    name = mapped_column(String(60))
    email = mapped_column(String(150), unique=True)
    password = mapped_column(String(150))
