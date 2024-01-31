from pydantic import BaseModel
from api_v1.subject.schemas import AllowedValuesByName

class BaseOrder(BaseModel):
    description: str | None = None
    is_active: bool | None = True
    subject_name: AllowedValuesByName
    user_id: int | None = None


class CreateOrder(BaseOrder):
    pass



