from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # For MVP, we use a fixed user_id (you can add auth later)
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")  # dummy
    db_project = models.Project(
        user_id=user_id,
        name=project.name,
        country=project.country,
        building_code=project.building_code
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    return project