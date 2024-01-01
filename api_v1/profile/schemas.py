from pydantic import BaseModel

class BaseProfile(BaseModel):
    fullname: str | None = None
    description: str | None = None


class CreateProfile(BaseProfile):
    pass

class ReadProfile(BaseProfile):
    pass


class ProfileUpdate(BaseProfile):
    pass


class UpdateProfile(BaseProfile):
    pass