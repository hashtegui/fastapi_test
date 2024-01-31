from datetime import datetime, timedelta
from typing import Any

import bcrypt
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt

from src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")


def create_access_token(self, *,
                        data: dict[str, Any],
                        expires_delta: int = 60):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm="HS256")
    return encoded_jwt


class AuthService:

    async def hash_password(self, password: str):
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt(rounds=10))
        return hashed_password.decode('utf-8')

    async def verify_password(self, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8'))

    def create_access_token(self, *,
                            data: dict[str, Any],
                            expires_delta: int = 60):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm="HS256")
        return encoded_jwt
