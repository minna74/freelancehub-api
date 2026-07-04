from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    nom: str
    client_id: int


class ProjectOut(BaseModel):
    id: int
    nom: str
    client_id: int
    freelance_id: int
    statut: str
    created_at: datetime

    model_config = {"from_attributes": True}