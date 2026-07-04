from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    freelance_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    statut = Column(String, nullable=False, default="actif")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", cascade="all, delete-orphan")