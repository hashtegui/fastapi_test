from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from jose import ExpiredSignatureError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import oauth2_scheme
from src.config.database.connection import get_db, sessionmanager
from src.config.settings import settings
from src.domain.models.funcionario.model import Funcionario
from src.domain.shared.users.model import User
from src.domain.shared.users.service import UserService


async def get_current_funcionario(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends()]
):
    try:
        decoded = jwt.decode(token, settings.secret, algorithms=["HS256"])

        user = await user_service.get_user_by_email(decoded["email"])

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")


async def get_current_schema(
    user: Annotated[User, Depends(get_current_funcionario)]

):
    engine = sessionmanager._engine
    if engine is None:
        raise

    async with sessionmanager.session(
            user.company.tenant.schema_name) as session:
        yield session


class Context:
    def __init__(self,
                 user: Annotated[User, Depends(get_current_funcionario)],
                 session: Annotated[AsyncSession,
                                    Depends(get_current_schema)]
                 ) -> None:
        self.session = session
        self.user = user

        self.funcionario: Optional[Funcionario] = None

    async def get_funcionario_atual(self):
        if self.funcionario is None:
            stm = await self.session.execute(select(Funcionario).where(
                Funcionario.user_id == self.user.id))

            self.funcionario = stm.scalars().first()

        return self.funcionario
