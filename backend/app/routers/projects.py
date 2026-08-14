from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
import uuid

router = APIRouter()

@router.get("/")
def list_projects(db: Session = Depends(get_db)):
    # હમણાં માટે ડમી યુઝર ID
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    projects = db.query(models.Project).filter(models.Project.user_id == user_id).all()
    return projects

@router.post("/")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    db_project = models.Project(
        id=uuid.uuid4(),
        user_id=user_id,
        name=project.name,
        country=project.country,
        building_code=project.building_code
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project