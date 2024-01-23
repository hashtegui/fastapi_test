from typing import List

from fastapi import APIRouter

from src.config.database.connection import SessionDB
from src.domain.shared.users import service
from src.domain.shared.users.schemas import UserIn, UserOut

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def get_users(session: SessionDB):
    return await service.get_users(session)


@router.get("/{user_id}")
async def get_user(user_id: str):
    return {"user": user_id}


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserIn, session: SessionDB):

    user = await service.create_user(user_in, session)

    return user
