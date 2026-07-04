from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_freelance, get_current_user
from app.core.permissions import get_client_ids_for_user
from app.models.client import Client
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_freelance),
):
    client = db.query(Client).filter(
        Client.id == project_in.client_id,
        Client.freelance_id == current_user.id,
    ).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client introuvable",
        )

    new_project = Project(
        nom=project_in.nom,
        client_id=project_in.client_id,
        freelance_id=current_user.id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.type == "freelance":
        return db.query(Project).filter(Project.freelance_id == current_user.id).all()

    client_ids = get_client_ids_for_user(db, current_user.id)
    return db.query(Project).filter(Project.client_id.in_(client_ids)).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.type == "freelance":
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.freelance_id == current_user.id,
        ).first()
    else:
        client_ids = get_client_ids_for_user(db, current_user.id)
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.client_id.in_(client_ids),
        ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet introuvable",
        )

    return project


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_freelance),
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.freelance_id == current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet introuvable",
        )

    project.nom = project_in.nom
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_freelance),
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.freelance_id == current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet introuvable",
        )

    db.delete(project)
    db.commit()