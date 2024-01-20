from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)
