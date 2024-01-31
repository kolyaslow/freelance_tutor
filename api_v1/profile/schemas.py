from pydantic import BaseModel

class BaseProfile(BaseModel):
    fullname: str | None = None
    description: str | None = None



class CreateProfile(BaseProfile):
    user_id: int | None = None

class ReadProfile(BaseProfile):
    pass


class UpdateProfile(BaseProfile):
    pass