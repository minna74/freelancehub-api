from datetime import datetime

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    nom: str
    email: EmailStr


class ClientOut(BaseModel):
    id: int
    nom: str
    email: EmailStr
    freelance_id: int
    user_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True