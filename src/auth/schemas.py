from fastapi import Form
from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    email: str = Form()
    password: str = Form()

    model_config = ConfigDict(from_attributes=True)
