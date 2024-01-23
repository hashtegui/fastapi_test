

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.shared.users.model import User
from src.domain.shared.users.schemas import UserIn


async def create_user(user_in: UserIn, session: AsyncSession):
    user = User(**user_in.model_dump())
    user.password = await hash_password(user_in.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession, limit: int = 100, offset: int = 0):
    result = await session.scalars(select(User).limit(limit).offset(offset))
    return result.all()


async def get_user_by_email(email: str, session: AsyncSession):
    result = await session.scalars(select(User).where(User.email == email))
    return result.first()


async def hash_password(password: str):
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt(rounds=10))
    return hashed_password.decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8'))
