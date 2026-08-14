from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.quantity_engine import calculate_quantities
from .. import models
import uuid

router = APIRouter()

@router.get("/{project_id}")
def get_quantities(project_id: uuid.UUID, db: Session = Depends(get_db)):
    # Check project exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    # Fetch all drawings for this project
    drawings = db.query(models.Drawing).filter(models.Drawing.project_id == project_id).all()
    if not drawings:
        raise HTTPException(404, "No drawings found for this project")
    
    # Gather all detected objects from all drawings
    all_objects = []
    for drawing in drawings:
        objects = db.query(models.DetectedObject).filter(models.DetectedObject.drawing_id == drawing.id).all()
        for obj in objects:
            all_objects.append({
                "type": obj.object_type,
                "geometry": obj.geometry,
                "properties": obj.properties
            })
    
    if not all_objects:
        raise HTTPException(404, "No detected objects found. Please run detection first.")
    
    # Calculate quantities using the quantity engine
    quantities = calculate_quantities(all_objects)
    
    # (Optional) Store quantities in the database for later use
    # For now, we just return the calculated quantities
    return quantities