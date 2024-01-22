from fastapi import APIRouter

from src.auth.schemas import LoginSchema

router = APIRouter(tags=['Auth'])


@router.post("/")
async def login(body: LoginSchema):
    # TODO implement login
    return {"email": body.email, "token": "supertoken", "permissions": ["admin"]}
