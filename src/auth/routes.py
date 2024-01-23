from fastapi import APIRouter, HTTPException

from src.auth import service
from src.auth.schemas import LoginSchema
from src.config.database.connection import SessionDB
from src.domain.shared.users import service as user_service

router = APIRouter(tags=['Auth'])


@router.post("/")
async def login(body: LoginSchema, session: SessionDB):

    user = await user_service.get_user_by_email(body.email, session)

    if user is None:
        raise HTTPException(404, 'User not found')

    if not await user_service.verify_password(body.password, user.password):
        raise HTTPException(401, 'Invalid credentials')

    token = service.create_access_token(data={"email": body.email})
    return {"email": user.email, "token": token, "permissions": ["user"]}
