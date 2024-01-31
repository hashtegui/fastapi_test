from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.auth.context import get_current_funcionario
from src.domain.shared.users.model import User
from src.domain.shared.users.schemas import UserIn, UserOut
from src.domain.shared.users.service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def get_users(users_service: Annotated[UserService, Depends()],
                    user: Annotated[User, Depends(get_current_funcionario)]):
    return await users_service.get_users()


@router.get("/{email}", response_model=UserOut)
async def get_user_by_email(
    email: str,
    users_service: Annotated[UserService, Depends()],
    user: Annotated[User, Depends(get_current_funcionario)]

):
    user_out = await users_service.get_user_by_email(email)

    if not user_out:
        raise HTTPException(status_code=404, detail="User not found")
    return user_out


@router.post("/", response_model=UserOut)
async def create_user(
        user_in: UserIn,
        users_service: Annotated[UserService, Depends()],
        user: Annotated[User, Depends(get_current_funcionario)]):

    user = await users_service.create_user(user_in)

    return user
