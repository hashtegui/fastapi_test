from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import LoginSchema
from src.auth.service import AuthService
from src.domain.shared.users.service import UserService

router = APIRouter(tags=['Auth'])


@router.post("/")
async def login(body: Annotated[OAuth2PasswordRequestForm, Depends()],
                user_service: Annotated[UserService, Depends()],
                auth_service: Annotated[AuthService, Depends()]):

    user = await user_service.get_user_by_email(body.username)

    if user is None:
        raise HTTPException(404, 'User not found')

    if not await auth_service.verify_password(body.password, user.password):
        raise HTTPException(401, 'Invalid credentials')

    token = auth_service.create_access_token(data={"email": body.username})
    return {"email": user.email, "access_token": token, "permissions": ["admin"]}
