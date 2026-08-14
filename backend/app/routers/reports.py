from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.report_generator import generate_excel, generate_pdf
from .. import models
import uuid
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/{project_id}/generate")
def generate_report(project_id: uuid.UUID, report_type: str = "excel", db: Session = Depends(get_db)):
    # Check project
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    # For MVP, we use dummy data. In production, fetch from DB.
    quantities = {
        "walls": {"gross": 45.2, "deduction": 3.8, "net": 41.4, "unit": "m³"},
        "flooring": {"gross": 120.5, "deduction": 0, "net": 120.5, "unit": "m²"},
        "plaster": {"gross": 380.5, "deduction": 39.7, "net": 340.8, "unit": "m²"},
        "painting": {"gross": 460.3, "deduction": 39.7, "net": 420.6, "unit": "m²"}
    }
    boq_items = [
        {"description": "Brickwork", "quantity": 41.4, "unit": "m³", "rate": 6500, "amount": 269100},
        {"description": "Flooring Tiles", "quantity": 120.5, "unit": "m²", "rate": 1200, "amount": 144600},
        {"description": "Internal Plaster", "quantity": 340.8, "unit": "m²", "rate": 250, "amount": 85200},
        {"description": "Wall Painting", "quantity": 420.6, "unit": "m²", "rate": 180, "amount": 75708}
    ]
    
    if report_type.lower() == "excel":
        excel_file = generate_excel(project, quantities, boq_items)
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=report_{project_id}.xlsx"}
        )
    elif report_type.lower() == "pdf":
        pdf_file = generate_pdf(project, quantities, boq_items)
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=report_{project_id}.pdf"}
        )
    else:
        raise HTTPException(400, "Invalid report type. Use 'excel' or 'pdf'.")