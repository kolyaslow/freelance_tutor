from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str



class UserUpdate(schemas.BaseUserUpdate):
    pass