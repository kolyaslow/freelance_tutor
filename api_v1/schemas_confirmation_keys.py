from pydantic import BaseModel


class CreateConfirmationKeys(BaseModel):
    user_id: int
    email_confirmation_code: str
