from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.detector import detect_objects
from .. import models
import uuid

router = APIRouter()   # ← આ લાઈન ખૂબ જ મહત્વપૂર્ણ છે

@router.post("/{drawing_id}/detect")
def detect_objects_in_drawing(drawing_id: uuid.UUID, db: Session = Depends(get_db)):
    # Check if drawing exists
    drawing = db.query(models.Drawing).filter(models.Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(404, "Drawing not found")
    
    # Get entities for this drawing
    entities = db.query(models.DrawingEntity).filter(models.DrawingEntity.drawing_id == drawing_id).all()
    if not entities:
        raise HTTPException(404, "No entities found for this drawing")
    
    # Convert to dict list for detector
    entities_dict = [
        {
            "type": e.entity_type,
            "layer": e.layer,
            "geometry": e.geometry,
            "properties": e.properties
        } for e in entities
    ]
    
    # Run detection
    detected = detect_objects(entities_dict)
    
    # Store detected objects in DB
    objects = []
    for obj in detected:
        db_obj = models.DetectedObject(
            id=uuid.uuid4(),
            drawing_id=drawing_id,
            object_type=obj["type"],
            confidence=obj.get("confidence", 0.8),
            geometry=obj.get("geometry", {}),
            properties=obj.get("properties", {}),
            verified=False
        )
        db.add(db_obj)
        objects.append(db_obj)
    
    db.commit()
    return objects