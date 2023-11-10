from enum import Enum

from fastapi_users import schemas
from pydantic import EmailStr


class Role(str, Enum):
    tutor = "репетитор"
    customer = "заказчик"

class UserRead(schemas.BaseUser[int]):
    role: Role


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    role: Role



class UserUpdate(schemas.BaseUserUpdate):
    pass