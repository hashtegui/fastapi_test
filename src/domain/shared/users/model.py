import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.shared import SharedBase

if TYPE_CHECKING:
    from src.domain.shared.company.model import Company


class User(SharedBase):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"))

    company: Mapped["Company"] = relationship(
        back_populates="user", lazy='joined')

    def to_funcionario(self):
        from src.domain.models.funcionario.model import Funcionario
        return Funcionario(nome=self.name, email=self.email, user_id=self.id)
