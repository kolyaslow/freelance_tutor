from enum import Enum

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr

from ..profile.schemas import ReadProfile


class Role(str, Enum):
    tutor = "tutor"
    customer = "customer"


class UserRead(schemas.BaseUser[int]):
    role: Role


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    role: Role


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserProfile(BaseModel):
    email: EmailStr
    role: Role
    profile: ReadProfile
