from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.config.database.connection import SessionDB
from src.domain.shared.users.schemas import UserIn, UserOut
from src.domain.shared.users.service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def get_users(users_service: Annotated[UserService, Depends()]):
    return await users_service.get_users()


@router.get("/{user_id}")
async def get_user(user_id: str):
    return {"user": user_id}


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserIn, users_service: Annotated[UserService, Depends()]):

    user = await users_service.create_user(user_in)

    return user
