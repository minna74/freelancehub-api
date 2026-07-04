from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    titre: str
    project_id: int
    priorite: str | None = None
    echeance: datetime | None = None


class TaskOut(BaseModel):
    id: int
    titre: str
    project_id: int
    statut: str
    priorite: str
    echeance: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}