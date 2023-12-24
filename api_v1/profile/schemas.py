from pydantic import BaseModel


class CreateProfile(BaseModel):
    fullname: str | None = None
    description: str | None = None


