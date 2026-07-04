from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_freelance, get_current_user
from app.core.permissions import get_client_ids_for_user
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_freelance),
):
    project = db.query(Project).filter(
        Project.id == task_in.project_id,
        Project.freelance_id == current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet introuvable",
        )

    new_task = Task(
        titre=task_in.titre,
        project_id=task_in.project_id,
        priorite=task_in.priorite or "moyenne",
        echeance=task_in.echeance,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.type == "freelance":
        return (
            db.query(Task)
            .join(Project)
            .filter(Project.freelance_id == current_user.id)
            .all()
        )

    client_ids = get_client_ids_for_user(db, current_user.id)
    project_ids = [
        p.id for p in db.query(Project).filter(Project.client_id.in_(client_ids)).all()
    ]
    return db.query(Task).filter(Task.project_id.in_(project_ids)).all()