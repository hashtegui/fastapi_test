from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.shared import SharedBase

if TYPE_CHECKING:
    from src.domain.shared.tenant.model import Tenant
    from src.domain.shared.users.model import User


class Company (SharedBase):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenant.id"))

    user: Mapped["User"] = relationship(back_populates="company")
    tenant: Mapped["Tenant"] = relationship(back_populates="company")
