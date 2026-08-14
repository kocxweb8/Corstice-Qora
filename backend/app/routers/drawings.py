from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..services.dxf_parser import parse_dxf
import os, shutil, uuid
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{project_id}/upload", response_model=schemas.DrawingUploadResponse)
def upload_dxf(project_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check project exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    # Save file
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ['dxf']:
        raise HTTPException(400, "Only DXF files are supported in MVP (convert DWG to DXF offline)")
    
    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}.dxf")
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Create drawing record
    drawing = models.Drawing(
        id=uuid.uuid4(),
        project_id=project_id,
        filename=file.filename,
        filepath=save_path,
        status="uploaded"
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)
    return drawing

@router.post("/{drawing_id}/parse")
def parse_drawing(drawing_id: uuid.UUID, db: Session = Depends(get_db)):
    drawing = db.query(models.Drawing).filter(models.Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(404, "Drawing not found")
    
    # Parse DXF
    entities = parse_dxf(drawing.filepath)
    
    # Store entities
    for ent in entities:
        db_entity = models.DrawingEntity(
            drawing_id=drawing_id,
            entity_type=ent["type"],
            layer=ent.get("layer", ""),
            geometry=ent.get("geometry", {}),
            properties=ent.get("properties", {})
        )
        db.add(db_entity)
    
    drawing.status = "parsed"
    db.commit()
    return {"status": "parsed", "entity_count": len(entities)}