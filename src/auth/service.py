from datetime import datetime, timedelta

from jose import jwt

from src.config.settings import settings


def create_access_token(*, data: dict, expires_delta: int = 60):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    print(settings.secret)
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm="HS256")
    return encoded_jwt
