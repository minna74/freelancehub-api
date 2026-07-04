from sqlalchemy.orm import Session

from app.models.client import Client


def get_client_ids_for_user(db: Session, user_id: int) -> list[int]:
    return [c.id for c in db.query(Client).filter(Client.user_id == user_id).all()]