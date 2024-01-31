

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from src.auth.service import AuthService
from src.config.database.connection import SessionDB, sessionmanager
from src.domain.shared.users.model import User
from src.domain.shared.users.schemas import UserIn


class UserService:

    def __init__(self,
                 session: SessionDB,
                 auth_service: Annotated[AuthService, Depends()],
                 ) -> None:
        self.auth_service = auth_service
        self.session = session

    async def create_user(self, user_in: UserIn):
        user = User(**user_in.model_dump())
        user.password = await self.auth_service.hash_password(user_in.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        schema_name = user.company.tenant.schema_name

        await self.session.close()

        async with sessionmanager.session(schema_name) as session:
            funcionario = user.to_funcionario()
            session.add(funcionario)
            await session.commit()
            await session.close()

        return user

    async def get_users(self,  limit: int = 100, offset: int = 0):
        result = await self.session.scalars(select(User).limit(limit).offset(offset))
        return result.all()

    async def get_user_by_email(self, email: str):
        result = await self.session.scalars(select(User).where(User.email == email))
        return result.first()
